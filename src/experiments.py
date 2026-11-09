"""Chuyển chỉ dẫn ID từ 1, chạy cùng điều kiện, báo cáo không xếp hạng bằng J."""
from dataclasses import asdict, dataclass

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
