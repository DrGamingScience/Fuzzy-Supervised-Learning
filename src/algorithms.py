"""Lõi tính toán độc lập UI; X: N×D, U: N×C, V: C×D.

Nguồn công thức: Endo et al. 2009 (2)–(14); Khang et al. 2021 (2)–(20).
Chỉ nhận thông tin giám sát đã tiết lộ, không nhận nhãn tham chiếu.
"""
from dataclasses import dataclass

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
