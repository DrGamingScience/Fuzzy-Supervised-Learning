"""Lõi tính toán độc lập UI; X: N×D, U: N×C, V: C×D.

Nguồn công thức: Endo et al. 2009 (2)–(14); Khang et al. 2021 (2)–(20).
Chỉ nhận thông tin giám sát đã tiết lộ, không nhận nhãn tham chiếu.
"""
from dataclasses import dataclass
from time import perf_counter

import numpy as np
from scipy.optimize import brentq
from scipy.special import expit, logsumexp

ALGORITHMS = ('fcm', 'ssfcm', 'ssfcm1', 'esfcm', 'ssmc')
ESFCM_WARNING = ('eSFCM theo công thức (14), lambda=1 trên dữ liệu gốc không khớp '
                 'Tables IV–V 2009; chưa xác định nguyên nhân, không ép khớp bảng.')


@dataclass(frozen=True)
class Config:
    algorithm: str = 'fcm'
    n_clusters: int = 2
    m: float = 2.0
    m_prime: float = 4.0
    lambda_: float = 1.0
    epsilon: float = 1e-7
    max_iter: int = 500
    seed: int = 42
    root_tol: float = 1e-12


def _integer(value, name, low, high=None):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise ValueError(f'{name} phải là số nguyên.')
    if value < low or (high is not None and value > high):
        raise ValueError(f'{name} ngoài miền cho phép [{low}, {high}].')


def _positive(value, name, lower=0, inclusive=False):
    try:
        ok = np.ndim(value) == 0 and np.isfinite(value) and (value >= lower if inclusive else value > lower)
    except TypeError:
        ok = False
    if not ok:
        raise ValueError(f'{name} phải hữu hạn và {">=" if inclusive else ">"} {lower}.')


def validate_inputs(X, config=Config(), initial_centers=None, B=None, targets=None):
    """Kiểm tra tham số áp dụng; trả bản sao, không sửa đầu vào người gọi."""
    if config.algorithm not in ALGORITHMS:
        raise ValueError('Thuật toán không hợp lệ.')
    try:
        X = np.array(X, dtype=float, copy=True)
    except (TypeError, ValueError) as exc:
        raise ValueError('X phải là ma trận số.') from exc
    if X.ndim != 2 or min(X.shape, default=0) == 0 or not np.isfinite(X).all():
        raise ValueError('X phải có shape (N,D), không rỗng và hữu hạn.')
    n, d = X.shape
    _integer(config.n_clusters, 'Số cụm', 2, n)
    _integer(config.max_iter, 'max_iter', 1)
    _integer(config.seed, 'seed', 0, 2**32-1)
    _positive(config.epsilon, 'epsilon')
    if config.algorithm in ('fcm', 'ssfcm', 'ssmc'):
        _positive(config.m, 'm', 1)
    if config.algorithm == 'ssmc':
        _positive(config.m_prime, "M'", config.m, inclusive=True)
        _positive(config.root_tol, 'root_tol')
        if config.root_tol >= 1:
            raise ValueError('root_tol phải nhỏ hơn 1.')
    if config.algorithm == 'esfcm':
        _positive(config.lambda_, 'lambda')
    c = config.n_clusters
    if initial_centers is None:
        V = X[np.random.default_rng(config.seed).choice(n, c, replace=False)].copy()
    else:
        V = np.array(initial_centers, dtype=float, copy=True)
        if V.shape != (c, d) or not np.isfinite(V).all():
            raise ValueError('Tâm đầu phải có shape (C,D) và hữu hạn.')
    prior = np.zeros((n, c))
    if config.algorithm in ('ssfcm', 'ssfcm1', 'esfcm') and B is not None:
        prior = np.array(B, dtype=float, copy=True)
        if (prior.shape != (n, c) or not np.isfinite(prior).all()
                or (prior < 0).any() or (prior > 1).any() or (prior.sum(axis=1) > 1).any()):
            raise ValueError('B phải có shape (N,C), thuộc [0,1], tổng hàng <= 1.')
    labels = np.full(n, -1, dtype=int)
    if config.algorithm == 'ssmc' and targets is not None:
        raw = np.asarray(targets)
        if (raw.shape != (n,) or raw.dtype.kind not in 'iu'
                or (raw < -1).any() or (raw >= c).any()):
            raise ValueError('Cụm đích phải là vector nguyên (N,), -1 hoặc 0..C-1.')
        labels = raw.astype(int, copy=True)
    return X, V, prior, labels


@dataclass
class Result:
    config: Config
    membership: np.ndarray
    centers: np.ndarray
    objective: float
    n_iter: int
    stop_reason: str
    elapsed_seconds: float
    warnings: tuple[str, ...] = ()

    @property
    def labels(self):
        return self.membership.argmax(axis=1)


def squared_distances(X, V):
    with np.errstate(over='ignore', invalid='ignore'):
        delta=X[:, None, :] - V[None, :, :]
        d2 = np.sum(delta**2, axis=2)
    if not np.isfinite(d2).all():
        raise ValueError('Khoảng cách vượt miền số thực; hãy đổi thang dữ liệu.')
    if ((d2==0)&np.any(delta!=0,axis=2)).any():
        raise ValueError('Khoảng cách bị underflow; hãy đổi thang dữ liệu.')
    return d2


def _fcm_membership(d2, m):
    """Khang 2021 (2); chia đều cho các tâm có khoảng cách bằng 0."""
    U = np.zeros_like(d2)
    zero = d2 == 0
    rows = zero.any(axis=1)
    U[rows] = zero[rows] / zero[rows].sum(axis=1, keepdims=True)
    logs = np.log(d2[~rows])
    # Trừ min trước chia: m gần 1 vẫn có ít nhất một logit bằng 0.
    with np.errstate(over='ignore', under='ignore'):
        weights = np.exp(-(logs-logs.min(axis=1,keepdims=True))/(m-1))
    U[~rows] = weights/weights.sum(axis=1,keepdims=True)
    return U


def update_membership(X, V, config, B=None, targets=None):
    d2 = squared_distances(X,V)
    if config.algorithm == 'esfcm':
        B = np.zeros_like(d2) if B is None else B
        # Endo (14): softmax ổn định, luôn có logit 0 ở cụm gần nhất.
        with np.errstate(over='ignore', under='ignore'):
            p=np.exp(-config.lambda_*(d2-d2.min(axis=1,keepdims=True)))
        return B+(1-B.sum(axis=1,keepdims=True))*p/p.sum(axis=1,keepdims=True)
    if config.algorithm in ('ssfcm', 'ssfcm1'):
        # Endo 2009 (6): B là cận dưới; tâm dùng phần dư theo (4).
        B = np.zeros_like(d2) if B is None else B
        if config.algorithm == 'ssfcm1':
            # (8): hòa chọn cụm có chỉ số nhỏ nhất, không chia cho m-1.
            base=np.eye(d2.shape[1])[d2.argmin(axis=1)]
        else:
            base=_fcm_membership(d2,config.m)
        return B+(1-B.sum(axis=1,keepdims=True))*base
    if config.algorithm == 'ssmc':
        U=_fcm_membership(d2,config.m)
        if targets is not None and config.m_prime != config.m:
            for i in np.flatnonzero(np.asarray(targets)>=0):
                U[i]=_ssmc_row(d2[i],int(targets[i]),config)
        return U
    if config.algorithm != 'fcm':
        raise NotImplementedError(config.algorithm)
    return _fcm_membership(d2,config.m)


def _ssmc_row(d2, k, config):
    """(17)–(20), giải (19) trong tọa độ logit của U_k.

    μ_j=(1/(M d_j²))^(1/(M-1)), S=sum_{j!=k} μ_j.
    Với q=μ_k/(μ_k+S): q^(M'-1)/(1-q)^(M-1)=1/(M' d_k² S^(M-1)).
    Hàm log đơn điệu, Brent có khoảng chặn; không ép nhãn sau phân cụm.
    """
    zero=d2==0
    if zero.any():
        return zero.astype(float)/zero.sum()
    logs=np.log(d2)-np.log(d2.min())  # (17) khoảng cách bình phương chuẩn hóa
    other=np.arange(len(d2))!=k
    log_mu=-(np.log(config.m)+logs[other])/(config.m-1)
    log_S=logsumexp(log_mu)
    constant=np.log(config.m_prime)+logs[k]+(config.m-1)*log_S
    def equation(z):
        return (-(config.m_prime-1)*np.logaddexp(0,-z)
                +(config.m-1)*np.logaddexp(0,z)+constant)
    bound=abs(constant)/min(config.m-1,config.m_prime-1)+2
    if not np.isfinite(bound):
        raise ValueError('Không lập được khoảng chặn nghiệm; tham số quá cực đoan.')
    z=brentq(equation,-bound,bound,xtol=config.root_tol,rtol=4*np.finfo(float).eps,maxiter=200)
    if abs(equation(z)) > max(1e-9,config.root_tol*max(config.m,config.m_prime)*4):
        raise ArithmeticError('Residual nghiệm sSMC vượt dung sai.')
    U=np.empty(len(d2))
    U[k]=expit(z)
    U[other]=expit(-z)*np.exp(log_mu-log_S)
    return U/U.sum()


def exponent_matrix(shape, config, targets):
    powers=np.full(shape,config.m,dtype=float)
    if targets is not None:
        rows=np.flatnonzero(np.asarray(targets)>=0)
        powers[rows,np.asarray(targets)[rows]]=config.m_prime
    return powers


def _weights(U, config, B, targets):
    if config.algorithm == 'esfcm':
        return U
    if config.algorithm in ('ssfcm', 'ssfcm1'):
        return np.abs(U-B)**(1 if config.algorithm=='ssfcm1' else config.m)
    if config.algorithm == 'ssmc':
        return U**exponent_matrix(U.shape,config,targets)
    return U**config.m


def objective(X, U, V, config, B=None, targets=None):
    value = float(np.sum(_weights(U,config,B,targets)*squared_distances(X,V)))
    if config.algorithm == 'esfcm':
        # (9): r log r, quy ước 0 log 0 = 0; nghiệm luôn U >= B.
        residual=U-(0 if B is None else B)
        positive=residual>0
        value += float(np.sum(residual[positive]*np.log(residual[positive]))/config.lambda_)
    if not np.isfinite(value):
        raise ValueError('Hàm mục tiêu vượt miền số thực.')
    return value


def _centers(X, weights, previous, warnings):
    V = previous.copy()
    for k in range(len(V)):
        scale = weights[:, k].max()
        if scale == 0:
            warnings.add(f'Cụm {k+1} mất trọng số; giữ tâm trước.')
        else:
            w = weights[:, k]/scale
            V[k] = (w/w.sum()) @ X
    return V


def _center_weights(U, config, B, targets, warnings):
    """Chuẩn hóa trọng số trong log trước lũy thừa, tránh mất cụm do underflow."""
    if config.algorithm=='esfcm':
        return U
    base=np.abs(U-B) if config.algorithm in ('ssfcm','ssfcm1') else U
    powers=(exponent_matrix(U.shape,config,targets) if config.algorithm=='ssmc'
            else 1 if config.algorithm=='ssfcm1' else config.m)
    with np.errstate(divide='ignore',over='ignore',invalid='ignore'):
        log_w=np.log(base)*powers
    if np.isnan(log_w).any() or np.isposinf(log_w).any() or (np.isneginf(log_w)&(base>0)).any():
        raise ValueError('Số mũ vượt miền tính toán trọng số; hãy giảm tham số.')
    weights=np.zeros_like(U)
    for k in range(U.shape[1]):
        top=log_w[:,k].max()
        if np.isfinite(top):
            weights[:,k]=np.exp(log_w[:,k]-top)
            if top < np.log(np.finfo(float).tiny):
                warnings.add(f'Cụm {k+1}: tính trọng số trong log để tránh underflow.')
    return weights


def _check_membership(U):
    if (not np.isfinite(U).all() or (U < 0).any() or (U > 1+1e-12).any()
            or not np.allclose(U.sum(axis=1),1,rtol=0,atol=1e-12)):
        raise ArithmeticError('U không hữu hạn hoặc vi phạm ràng buộc simplex.')


def fit(X, config=Config(), initial_centers=None, B=None, targets=None):
    """Dừng khi max_k ||V_k mới - V_k cũ||₂ <= epsilon, hoặc max_iter.

    U cuối luôn được tính lại từ đúng V cuối. Tâm mất trọng số giữ nguyên.
    """
    start=perf_counter()
    X,V,B,targets=validate_inputs(X,config,initial_centers,B,targets)
    warnings=set()
    if config.algorithm == 'esfcm':
        warnings.add(ESFCM_WARNING)
    U=update_membership(X,V,config,B,targets)
    _check_membership(U)
    reason='max_iter'
    for iteration in range(1,config.max_iter+1):
        new=_centers(X,_center_weights(U,config,B,targets,warnings),V,warnings)
        if not np.isfinite(new).all():
            raise ValueError('Tâm vượt miền số thực; hãy đổi thang dữ liệu.')
        shift=float(np.max(np.hypot.reduce(new-V,axis=1)))
        V=new
        U=update_membership(X,V,config,B,targets)
        _check_membership(U)
        if shift <= config.epsilon:
            reason='epsilon'
            break
    return Result(config,U.copy(),V.copy(),objective(X,U,V,config,B,targets),
                  iteration,reason,perf_counter()-start,tuple(sorted(warnings)))
