"""Kiểm chứng mã src mới, không dùng tính thử khảo sát làm kết quả test."""
from dataclasses import replace

import numpy as np
import pytest

from src.algorithms import Config, validate_inputs
from src.data import demo_initial_centers, load_paper_data, membership_preset
from src.algorithms import fit, update_membership, objective


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


def test_fcm_paper_and_independent_one_step():
    X,_=load_paper_data(); V=demo_initial_centers(); c=Config()
    U=update_membership(X,V,c)
    d2=((X[:,None]-V)**2).sum(axis=2)
    expected=(1/d2)/(1/d2).sum(axis=1,keepdims=True)
    np.testing.assert_allclose(U,expected)
    r=fit(X,c,V)
    assert r.stop_reason=='epsilon' and 1<r.n_iter<500
    assert r.membership[8,0]==pytest.approx(0.188663,abs=1e-6)
    # 2021 trang 10: (2.719,5), (9.018,5), dung sai theo chữ số in.
    np.testing.assert_allclose(r.centers,[[2.719,5],[9.018,5]],atol=0.001)
    np.testing.assert_allclose(r.membership.sum(axis=1),1,atol=1e-14)
    assert np.isfinite(r.objective) and (r.membership>=0).all()
    np.testing.assert_allclose(r.membership,update_membership(X,r.centers,c))
    limited=fit(X,replace(c,max_iter=1),V)
    assert limited.stop_reason=='max_iter' and limited.n_iter==1


def test_fcm_seed_and_zero_distance():
    X=np.array([[0.,0],[0,0],[2,0],[4,0]])
    U=update_membership(X,np.array([[0.,0],[0,0]]),Config())
    np.testing.assert_allclose(U,0.5)
    np.testing.assert_array_equal(fit(X).centers,fit(X).centers)


@pytest.mark.parametrize('level,expected', [(0,0.188663),(0.3,0.451669),(0.6,0.693818)])
def test_ssfcm_paper_and_weighted_centers(level,expected):
    X,_=load_paper_data(); V=demo_initial_centers(); B=membership_preset(level)
    c=Config(algorithm='ssfcm')
    r=fit(X,c,V,B)
    assert r.membership[8,0]==pytest.approx(expected,abs=1e-6)
    assert (r.membership>=B).all()
    np.testing.assert_allclose(r.membership.sum(axis=1),1)
    initial=update_membership(X,V,c,B)
    w=(initial-B)**2
    expected_V=(w.T@X)/w.sum(axis=0)[:,None]
    one=fit(X,replace(c,max_iter=1),V,B)
    np.testing.assert_allclose(one.centers,expected_V)
    if level==0:
        np.testing.assert_array_equal(r.membership,fit(X,Config(),V).membership)


@pytest.mark.parametrize('level',[0,0.3,0.6])
def test_ssfcm1_full_table_iii(level):
    X,_=load_paper_data(); c=Config(algorithm='ssfcm1',m=1)
    B=membership_preset(level)
    r=fit(X,c,demo_initial_centers(),B)
    # Table III 2009, trang PDF 6: ID 1–8 → 1; 9,10 → (B,1-B); 11–20 → 2.
    expected=np.zeros((20,2)); expected[:8,0]=1
    expected[8:10]=[level,1-level]; expected[10:,1]=1
    np.testing.assert_array_equal(r.membership,expected)
    w=np.abs(expected-B)
    np.testing.assert_allclose(r.centers,(w.T@X)/w.sum(axis=0)[:,None])


def test_ssfcm1_tie_uses_first_cluster():
    X=np.array([[1.,0],[3,0]])
    U=update_membership(X,np.array([[0.,0],[2,0]]),Config(algorithm='ssfcm1',m=1))
    np.testing.assert_array_equal(U,[[1,0],[0,1]])


def test_esfcm_formula_entropy_centers_and_reported_discrepancy():
    X,_=load_paper_data(); V=demo_initial_centers(); B=membership_preset(0.3)
    c=Config(algorithm='esfcm',lambda_=0.04)
    d2=((X[:,None]-V)**2).sum(axis=2)
    p=np.exp(-c.lambda_*d2); p/=p.sum(axis=1,keepdims=True)
    expected=B+(1-B.sum(axis=1,keepdims=True))*p
    np.testing.assert_allclose(update_membership(X,V,c,B),expected)
    one=fit(X,replace(c,max_iter=1),V,B)
    np.testing.assert_allclose(one.centers,(expected.T@X)/expected.sum(axis=0)[:,None])
    r=expected-B
    ent=sum(v*np.log(v) for v in r.flat if v>0)
    assert objective(X,expected,V,c,B)==pytest.approx((expected*d2).sum()+ent/c.lambda_)
    # Thay trực tiếp tâm Table V vào (14): U1,2 ~ 1.13e-21, không phải 0.24.
    table_V=np.array([[4.6,5],[8.33,5]])
    actual=update_membership(X,table_V,replace(c,lambda_=1))
    assert actual[0,1]==pytest.approx(1.133e-21,rel=0.005,abs=0)
    assert any('không khớp' in w for w in one.warnings)


def test_esfcm_stable_softmax_and_zero_entropy():
    X=np.array([[0.,0],[1,1]])
    c=Config(algorithm='esfcm',lambda_=1e308)
    B=np.array([[1.,0],[0,1.]])
    r=fit(X,c,X,B)
    np.testing.assert_array_equal(r.membership,B)
    assert r.objective==0
