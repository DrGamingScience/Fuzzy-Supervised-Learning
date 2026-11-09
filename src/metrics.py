"""Metrics phân hoạch cứng theo Vendramin et al. 2010, mục 2.

Tâm được tính từ nhãn cứng, không nhận tâm mờ của thuật toán.
Giá trị không xác định được giữ None kèm lý do, không thay bằng 0.
"""
from dataclasses import dataclass

import numpy as np
from scipy.spatial.distance import cdist


@dataclass(frozen=True)
class Metric:
    value: float | None
    direction: str = 'max'
    reason: str | None = None


def _metric(value, direction='max', reason='Kết quả vượt miền số thực.'):
    return Metric(float(value),direction) if np.isfinite(value) else Metric(None,direction,reason)


def _labels(labels, n=None):
    y=np.asarray(labels)
    if y.ndim!=1 or (n is not None and len(y)!=n):
        raise ValueError('Nhãn phải là vector có cùng số điểm.')
    if y.dtype.kind in 'fc' and not np.isfinite(y).all():
        raise ValueError('Nhãn không được NaN/Inf.')
    if any(v is None or (isinstance(v,str) and not v) for v in y):
        raise ValueError('Nhãn không được rỗng.')
    return y


def geometric_metrics(X, labels):
    X=np.asarray(X,dtype=float)
    if X.ndim!=2 or min(X.shape,default=0)==0 or not np.isfinite(X).all():
        raise ValueError('X phải là ma trận hữu hạn, không rỗng.')
    labels=_labels(labels,len(X))
    _,y=np.unique(labels,return_inverse=True)
    n=len(X); k=int(y.max())+1
    names=('silhouette','ch','db','dunn','pbm')
    if not 2<=k<n:
        return {name:Metric(None,'min' if name=='db' else 'max',
                           'Cần 2 <= số cụm cứng thực tế < số điểm.') for name in names}
    groups=[np.flatnonzero(y==j) for j in range(k)]
    centers=np.array([X[idx].mean(axis=0) for idx in groups])
    distance=cdist(X,X); center_distance=cdist(centers,centers)
    if not np.isfinite(distance).all() or not np.isfinite(center_distance).all():
        raise ValueError('Khoảng cách metrics vượt miền số thực; hãy đổi thang dữ liệu.')
    # SWC: singleton có silhouette=0; khoảng cách Euclid, không bình phương.
    silhouettes=[]
    for i in range(n):
        own=groups[y[i]]
        if len(own)==1:
            silhouettes.append(0.0); continue
        a=distance[i,own].sum()/(len(own)-1)
        b=min(distance[i,g].mean() for j,g in enumerate(groups) if j!=y[i])
        silhouettes.append((b-a)/max(a,b) if max(a,b)>0 else 0.0)
    residual=X-centers[y]
    within=float(np.sum(residual**2))
    between=float(sum(len(g)*np.sum((centers[j]-X.mean(axis=0))**2) for j,g in enumerate(groups)))
    ch=_metric((between/(k-1))/(within/(n-k))) if within>0 else Metric(None,'max','Tổng bình phương nội cụm bằng 0.')
    scatter=np.array([np.linalg.norm(residual[g],axis=1).mean() for g in groups])
    off=~np.eye(k,dtype=bool)
    if (center_distance[off]==0).any():
        db=Metric(None,'min','Có hai tâm cứng trùng nhau.')
    else:
        ratios=np.full((k,k),-np.inf)
        ratios[off]=(scatter[:,None]+scatter[None,:])[off]/center_distance[off]
        db=_metric(ratios.max(axis=1).mean(),'min')
    diameter=max(distance[np.ix_(g,g)].max() for g in groups)
    separation=min(distance[np.ix_(g,h)].min() for i,g in enumerate(groups) for h in groups[i+1:])
    dunn=_metric(separation/diameter) if diameter>0 else Metric(None,'max','Đường kính nội cụm lớn nhất bằng 0.')
    # PBM: ((E1/Ek) * Dk/k)^2; E là tổng khoảng cách Euclid tới tâm cứng.
    E1=np.linalg.norm(X-X.mean(axis=0),axis=1).sum()
    Ek=np.linalg.norm(residual,axis=1).sum()
    with np.errstate(over='ignore',invalid='ignore'):
        pbm=_metric(((E1/Ek)*center_distance.max()/k)**2) if Ek>0 else Metric(None,'max','Tổng khoảng cách nội cụm bằng 0.')
    return dict(silhouette=_metric(np.mean(silhouettes)),ch=ch,db=db,dunn=dunn,pbm=pbm)
