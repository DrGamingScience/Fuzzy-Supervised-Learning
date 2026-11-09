"""Đối chiếu bảng nguồn và bộ tối ưu độc lập, không tái dùng cập nhật của src."""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy.optimize import minimize
from scipy.special import xlogy

from src.algorithms import Config, fit, update_membership
from src.data import load_paper_data, demo_initial_centers, membership_preset, ssmc_preset


@pytest.mark.parametrize('column,algorithm,level,mp',[
    ('fcm','fcm',0,2),('ssfcm_03','ssfcm',0.3,2),('ssfcm_06','ssfcm',0.6,2),
    ('ssmc_4','ssmc',0,4),('ssmc_8','ssmc',0,8)])
def test_full_paper_memberships(column,algorithm,level,mp):
    source=pd.read_csv(Path(__file__).parent/'fixtures/paper_memberships.csv')
    X,_=load_paper_data()
    r=fit(X,Config(algorithm=algorithm,m_prime=mp),demo_initial_centers(),
          membership_preset(level),np.array(ssmc_preset(mp).targets))
    # Bảng làm tròn 2 chữ số: sai số tối đa 0.005; không so số vòng.
    checked=np.ones(20,dtype=bool)
    if column=='ssmc_4':
        # Sai khác nguồn có test riêng bên dưới, không nới dung sai cả bảng.
        checked[[16,18]]=False
    np.testing.assert_allclose(r.membership[checked,0],source[column][checked],rtol=0,atol=0.005)
    np.testing.assert_allclose(r.membership[checked,1],1-source[column][checked],rtol=0,atol=0.005)


def test_2021_table3_rows17_19_rounding_discrepancy():
    source=pd.read_csv(Path(__file__).parent/'fixtures/paper_memberships.csv')
    X,_=load_paper_data()
    # (15), không giám sát ở ID 17/19: 1/d² chuẩn hóa; tâm do bài công bố trang 10.
    V=np.array([[2.735,5],[9.200,5]])
    d=((X[[16,18],None]-V)**2).sum(axis=2)
    independent=(1/d)/(1/d).sum(axis=1,keepdims=True)
    np.testing.assert_allclose(independent[:,0],0.10452027,atol=1e-8)
    np.testing.assert_array_equal(source['ssmc_4'].iloc[[16,18]],[0.11,0.11])
    assert (np.abs(independent[:,0]-source['ssmc_4'].iloc[[16,18]])>0.005).all()
    r=fit(X,Config(algorithm='ssmc',m_prime=4),demo_initial_centers(),
          targets=np.array(ssmc_preset(4).targets))
    np.testing.assert_allclose(r.membership[[16,18],0],0.10451687,atol=1e-8)


@pytest.mark.parametrize('algorithm',['fcm','ssfcm','ssfcm1','esfcm','ssmc'])
def test_memberships_minimize_independent_objective(algorithm):
    rng=np.random.default_rng(701)
    X=rng.normal(size=(6,2)); V=rng.normal(size=(3,2))
    B=np.zeros((6,3)); B[:,1]=0.3
    c=Config(algorithm=algorithm,n_clusters=3,m=1.7,m_prime=5.3,lambda_=0.7)
    targets=np.array([0,1,2,0,1,2]); U=update_membership(X,V,c,B,targets)
    for i in range(len(X)):
        d=((X[i]-V)**2).sum(axis=1)
        lower=B[i] if algorithm in ('ssfcm','ssfcm1','esfcm') else np.zeros(3)
        p=np.full(3,c.m); p[targets[i]]=c.m_prime
        def cost(u):
            if algorithm=='esfcm':
                return u@d+xlogy(u-lower,u-lower).sum()/c.lambda_
            if algorithm in ('ssfcm','ssfcm1'):
                return (np.abs(u-lower)**(1 if algorithm=='ssfcm1' else c.m))@d
            return (u**(p if algorithm=='ssmc' else c.m))@d
        reference=minimize(cost,lower+(1-lower.sum())/3,method='SLSQP',
                           bounds=list(zip(lower,np.ones(3))),
                           constraints={'type':'eq','fun':lambda u:u.sum()-1},
                           options={'ftol':1e-12,'maxiter':1000})
        assert reference.success, reference.message
        assert cost(U[i])==pytest.approx(reference.fun,abs=2e-7)
