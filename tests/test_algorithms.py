"""Kiểm chứng mã src mới, không dùng tính thử khảo sát làm kết quả test."""
from dataclasses import replace

import numpy as np
import pytest

from src.algorithms import Config, validate_inputs
from src.data import demo_initial_centers, load_paper_data


@pytest.mark.parametrize('X', [[], [1,2], [[np.nan]], [[np.inf]], np.empty((2,0)), [['x']]])
def test_invalid_data(X):
    with pytest.raises(ValueError, match='X'):
        validate_inputs(X)


@pytest.mark.parametrize('change', [dict(n_clusters=1),dict(n_clusters=21),dict(n_clusters=2.5),
    dict(m=1),dict(m=np.inf),dict(max_iter=0),dict(max_iter=True),dict(seed=-1),
    dict(epsilon=0),dict(algorithm='other')])
def test_invalid_config(change):
    with pytest.raises(ValueError):
        validate_inputs(load_paper_data()[0], replace(Config(), **change))


@pytest.mark.parametrize('B', [np.zeros((19,2)),np.full((20,2),0.6),np.full((20,2),-0.1),np.full((20,2),np.nan)])
def test_invalid_prior(B):
    with pytest.raises(ValueError, match='B'):
        validate_inputs(load_paper_data()[0], Config(algorithm='ssfcm'), B=B)


def test_algorithm_specific_validation_and_copies():
    X,_=load_paper_data(); V=demo_initial_centers()
    a,v,b,t=validate_inputs(X,Config(m_prime=-5,lambda_=-1),V,B='ignored',targets='ignored')
    a[:]=0; v[:]=0
    assert X[2,0] == 1.75 and V[0,0] == 2.7
    validate_inputs(X,Config(algorithm='esfcm',m=1,m_prime=-10))
    validate_inputs(X,Config(algorithm='ssfcm1',m=1))
    with pytest.raises(ValueError, match="M'"):
        validate_inputs(X,Config(algorithm='ssmc',m_prime=1))
    with pytest.raises(ValueError, match='lambda'):
        validate_inputs(X,Config(algorithm='esfcm',lambda_=0))
    with pytest.raises(ValueError, match='Tâm'):
        validate_inputs(X, initial_centers=np.zeros((2,3)))
    for targets in [np.zeros(20), [2]*20, [-2]*20, [0]*19]:
        with pytest.raises(ValueError, match='đích'):
            validate_inputs(X,Config(algorithm='ssmc'),targets=targets)
