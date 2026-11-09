"""Chuyển chỉ dẫn ID từ 1, chạy cùng điều kiện, báo cáo không xếp hạng bằng J."""
from dataclasses import asdict, dataclass
import io
import json
import zipfile

import numpy as np
import pandas as pd

from src.algorithms import Config, Result, fit, validate_inputs
from src.metrics import metric_report, supervision_mask


def _id(value, name, maximum):
    if (isinstance(value,(bool,np.bool_)) or not isinstance(value,(int,float,np.integer,np.floating))
            or not np.isfinite(value) or value!=int(value) or not 1<=value<=maximum):
        raise ValueError(f'{name} phải là số nguyên từ 1 đến {maximum}.')
    return int(value)-1


def supervision_from_rows(rows, n, c, use_membership=True):
    """Một điểm tối đa một chỉ dẫn bật; dòng tắt không có tác dụng.

    B là mức độ thuộc cho sS/eS. Cụm đích cho sSMC độc lập với B và M'.
    Với sSMC riêng, use_membership=False để không áp validation B không áp dụng.
    """
    records=rows.to_dict('records') if isinstance(rows,pd.DataFrame) else rows
    B=np.zeros((n,c)); targets=np.full(n,-1,dtype=int); seen=set()
    for row in records:
        enabled=row.get('enabled',False)
        if not isinstance(enabled,(bool,np.bool_)):
            raise ValueError('Bật/tắt phải là giá trị boolean.')
        if not enabled: continue
        i=_id(row.get('point_id'),'ID điểm',n)
        k=_id(row.get('target_cluster'),'Cụm đích',c)
        if i in seen:
            raise ValueError(f'ID điểm {i+1} có chỉ dẫn bật trùng nhau.')
        seen.add(i); targets[i]=k
        if use_membership:
            b=row.get('membership')
            if (isinstance(b,(bool,np.bool_)) or not isinstance(b,(int,float,np.number))
                    or not np.isfinite(b) or not 0<=b<=1):
                raise ValueError(f'B của điểm {i+1} phải hữu hạn trong [0,1].')
            B[i,k]=float(b)
    return B,targets


@dataclass
class Experiment:
    X: np.ndarray
    reference: np.ndarray | None
    initial_centers: np.ndarray
    B: np.ndarray
    targets: np.ndarray
    results: dict[str,Result]
    reports: dict


def run_experiment(X, configs, initial_centers=None, B=None, targets=None, reference=None):
    configs=tuple(configs)
    if not configs or len({c.algorithm for c in configs})!=len(configs):
        raise ValueError('Cần ít nhất một cấu hình, không trùng thuật toán.')
    if len({c.n_clusters for c in configs})!=1:
        raise ValueError('So sánh phải dùng cùng số cụm.')
    # Tạo tâm chung một lần theo seed cấu hình đầu, kể cả khi các cấu hình có seed khác.
    X,V,_,_=validate_inputs(X,configs[0],initial_centers,B,targets)
    for config in configs:
        validate_inputs(X,config,V,B,targets)
    prior=np.zeros((len(X),configs[0].n_clusters)) if B is None else np.array(B,dtype=float,copy=True)
    target=np.full(len(X),-1,dtype=int) if targets is None else np.array(targets,copy=True)
    ref=None if reference is None else np.array(reference,copy=True)
    if ref is not None and (ref.shape!=(len(X),) or (ref.dtype.kind in 'fc' and not np.isfinite(ref).all())):
        raise ValueError('Nhãn tham chiếu phải là vector hữu hạn có cùng số điểm.')
    results={}; reports={}
    for config in configs:
        result=fit(X,config,V,prior,target)
        mask=supervision_mask(config.algorithm,len(X),prior,target)
        results[config.algorithm]=result
        reports[config.algorithm]=metric_report(X,result.labels,ref,mask)
    return Experiment(X,ref,V.copy(),prior,target,results,reports)


def comparison_table(experiment):
    """J khác định nghĩa nên không đưa vào bảng so sánh/xếp hạng."""
    rows=[]
    for name,result in experiment.results.items():
        row=dict(algorithm=name,parameters=asdict(result.config),n_iter=result.n_iter,
                 elapsed_seconds=result.elapsed_seconds,stop_reason=result.stop_reason,
                 warnings='; '.join(result.warnings))
        for scope,metrics in experiment.reports[name].items():
            for metric,value in metrics.items():
                key=f'{scope}.{metric}'
                row[key]=value.value; row[key+'.reason']=value.reason
        rows.append(row)
    return pd.DataFrame(rows)


def experiment_payload(experiment):
    payload=dict(schema_version=1,id_convention='ID điểm/cụm từ 1; nhãn tham chiếu giữ nguyên mã gốc.',
                 X=experiment.X.tolist(),reference=None if experiment.reference is None else experiment.reference.tolist(),
                 initial_centers=experiment.initial_centers.tolist(),B=experiment.B.tolist(),
                 targets=[None if v<0 else int(v)+1 for v in experiment.targets],results={})
    for name,result in experiment.results.items():
        payload['results'][name]=dict(config=asdict(result.config),membership=result.membership.tolist(),
            centers=result.centers.tolist(),labels=(result.labels+1).tolist(),objective=result.objective,
            n_iter=result.n_iter,stop_reason=result.stop_reason,elapsed_seconds=result.elapsed_seconds,
            warnings=list(result.warnings),supervised=supervision_mask(name,len(experiment.X),experiment.B,experiment.targets).tolist(),
            metrics={scope:{metric:asdict(value) for metric,value in metrics.items()}
                     for scope,metrics in experiment.reports[name].items()},
            history=[dict(iteration=s.iteration,membership=s.membership.tolist(),centers=s.centers.tolist(),
                          objective=s.objective,center_shift=s.center_shift) for s in result.history])
    return payload


def export_zip(experiment):
    """ZIP tự chứa JSON strict + CSV UTF-8 BOM, gồm mọi snapshot và cấu hình."""
    payload=experiment_payload(experiment)
    output=io.BytesIO()
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('result.json',json.dumps(payload,ensure_ascii=False,indent=2,allow_nan=False).encode('utf-8'))
        archive.writestr('HUONG_DAN.txt',
            ('Kết quả phân cụm mờ bán giám sát\nCSV: UTF-8 BOM. ID điểm/cụm từ 1; nhãn tham chiếu giữ mã gốc.\n'
             'Vòng 0: tâm khởi tạo, U tính từ tâm này. J chỉ theo dõi từng thuật toán, không xếp hạng chéo.\n'
             'Chỉ dẫn B và M\' có ý nghĩa khác nhau. X không chứa nhãn tham chiếu.\n'
             'eSFCM theo công thức, có sai khác Tables IV-V 2009; xem warnings và docs/VALIDATION.md.\n'
             '2021 Table 3 M\'=4, ID 17/19 in 0.11; công thức tại tâm nguồn cho 0.10452.\n').encode('utf-8-sig'))
        def csv(name,frame):
            archive.writestr(name,frame.to_csv(index=False).encode('utf-8-sig'))
        data=pd.DataFrame(experiment.X,columns=[f'x{d+1}' for d in range(experiment.X.shape[1])])
        data.insert(0,'point_id',np.arange(1,len(data)+1))
        if experiment.reference is not None: data['reference']=experiment.reference
        csv('data.csv',data)
        supervision=pd.DataFrame(experiment.B,columns=[f'B{k+1}' for k in range(experiment.B.shape[1])])
        supervision.insert(0,'point_id',np.arange(1,len(data)+1))
        supervision['target_cluster']=pd.array([None if t<0 else int(t)+1 for t in experiment.targets],dtype='Int64')
        csv('supervision.csv',supervision)
        csv('comparison.csv',comparison_table(experiment).drop(columns='parameters'))
        for name,result in experiment.results.items():
            members=[]; centers=[]; history=[]; metrics=[]
            for s in result.history:
                for i,u in enumerate(s.membership):
                    members.append(dict(iteration=s.iteration,point_id=i+1,cluster=int(u.argmax())+1,
                                        **{f'U{k+1}':float(v) for k,v in enumerate(u)}))
                for k,v in enumerate(s.centers):
                    centers.append(dict(iteration=s.iteration,cluster=k+1,**{f'x{d+1}':float(x) for d,x in enumerate(v)}))
                history.append(dict(iteration=s.iteration,objective=s.objective,center_shift=s.center_shift))
            for scope,values in experiment.reports[name].items():
                for metric,value in values.items():
                    metrics.append(dict(scope=scope,metric=metric,**asdict(value)))
            csv(f'{name}/memberships.csv',pd.DataFrame(members))
            csv(f'{name}/centers.csv',pd.DataFrame(centers))
            csv(f'{name}/history.csv',pd.DataFrame(history))
            csv(f'{name}/metrics.csv',pd.DataFrame(metrics))
    return output.getvalue()
