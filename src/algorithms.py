"""Lõi tính toán độc lập UI; X: N×D, U: N×C, V: C×D.

Nguồn công thức: Endo et al. 2009 (2)–(14); Khang et al. 2021 (2)–(20).
Chỉ nhận thông tin giám sát đã tiết lộ, không nhận nhãn tham chiếu.
"""
from dataclasses import dataclass
from time import perf_counter

import numpy as np

ALGORITHMS = ('fcm', 'ssfcm', 'ssfcm1', 'esfcm', 'ssmc')


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
        d2 = np.sum((X[:, None, :] - V[None, :, :])**2, axis=2)
    if not np.isfinite(d2).all():
        raise ValueError('Khoảng cách vượt miền số thực; hãy đổi thang dữ liệu.')
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
    if config.algorithm == 'ssfcm':
        # Endo 2009 (6): B là cận dưới; tâm dùng phần dư theo (4).
        B = np.zeros_like(d2) if B is None else B
        return B+(1-B.sum(axis=1,keepdims=True))*_fcm_membership(d2,config.m)
    if config.algorithm != 'fcm':
        raise NotImplementedError(config.algorithm)
    return _fcm_membership(d2,config.m)


def _weights(U, config, B, targets):
    if config.algorithm == 'ssfcm':
        return np.abs(U-B)**config.m
    return U**config.m


def objective(X, U, V, config, B=None, targets=None):
    value = float(np.sum(_weights(U,config,B,targets)*squared_distances(X,V)))
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


def fit(X, config=Config(), initial_centers=None, B=None, targets=None):
    """Dừng khi max_k ||V_k mới - V_k cũ||₂ <= epsilon, hoặc max_iter.

    U cuối luôn được tính lại từ đúng V cuối. Tâm mất trọng số giữ nguyên.
    """
    start=perf_counter()
    X,V,B,targets=validate_inputs(X,config,initial_centers,B,targets)
    warnings=set()
    U=update_membership(X,V,config,B,targets)
    reason='max_iter'
    for iteration in range(1,config.max_iter+1):
        new=_centers(X,_weights(U,config,B,targets),V,warnings)
        shift=float(np.max(np.linalg.norm(new-V,axis=1)))
        V=new
        U=update_membership(X,V,config,B,targets)
        if shift <= config.epsilon:
            reason='epsilon'
            break
    return Result(config,U.copy(),V.copy(),objective(X,U,V,config,B,targets),
                  iteration,reason,perf_counter()-start,tuple(sorted(warnings)))
