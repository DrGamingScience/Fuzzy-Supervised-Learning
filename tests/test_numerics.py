"""Các biên số học thực sự chạy trên lõi; lỗi miền số phải báo rõ."""
import numpy as np
import pytest

from src.algorithms import ALGORITHMS, Config, fit, update_membership


@pytest.mark.parametrize('algorithm',ALGORITHMS)
def test_coincident_points_and_centers(algorithm):
    X=np.array([[0.,0],[0,0],[0,0],[0,0]])
    c=Config(algorithm=algorithm)
    r=fit(X,c,X[:2],B=np.zeros((4,2)),targets=np.array([0,1,-1,-1]))
    assert np.isfinite(r.membership).all() and np.isfinite(r.centers).all()
    np.testing.assert_allclose(r.membership.sum(axis=1),1)
    # eSFCM (9) còn hạng entropy: 4 hàng × 2 × 0.5 log(0.5).
    assert r.objective==pytest.approx(-4*np.log(2) if algorithm=='esfcm' else 0)


@pytest.mark.parametrize('algorithm',['ssfcm','ssfcm1','esfcm'])
def test_fully_fixed_prior_and_empty_residual_cluster(algorithm):
    X=np.array([[0.,0],[2,0],[10,0]])
    B=np.array([[1.,0],[1,0],[1,0]])
    V=np.array([[1.,0],[9,0]])
    r=fit(X,Config(algorithm=algorithm),V,B)
    np.testing.assert_array_equal(r.membership,B)
    if algorithm!='esfcm':
        np.testing.assert_array_equal(r.centers,V)
        assert len(r.warnings)==2
    else:
        np.testing.assert_allclose(r.centers[0],X.mean(axis=0))
        assert any('mất trọng số' in w for w in r.warnings)


@pytest.mark.parametrize('algorithm',['fcm','ssfcm','ssmc'])
def test_extreme_exponent_retains_finite_centers(algorithm):
    X=np.array([[0.,0],[1,0],[3,0],[7,0]])
    r=fit(X,Config(algorithm=algorithm,m=10000,m_prime=20000),
          np.array([[0.,1],[7,1]]),targets=np.array([0,-1,-1,1]))
    assert np.isfinite(r.centers).all() and np.isfinite(r.membership).all()
    np.testing.assert_allclose(r.membership.sum(axis=1),1,atol=1e-12)
    assert any('log' in w for w in r.warnings)


def test_extreme_scale_reports_error_instead_of_nan_or_false_zero():
    for size in [1e200,1e-200]:
        with pytest.raises(ValueError,match='Khoảng cách'):
            fit(np.array([[0.,0],[size,0]]),initial_centers=np.array([[0.,0],[size,0]]))


def test_near_one_fuzzifier_and_multiple_zero_centers():
    X=np.array([[0.,0],[1,0],[2,0]])
    V=np.array([[0.,0],[0,0]])
    U=update_membership(X,V,Config(m=np.nextafter(1.,2.)))
    np.testing.assert_allclose(U,0.5)
