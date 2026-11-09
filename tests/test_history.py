import numpy as np
import pytest

from src.algorithms import ALGORITHMS, Config, fit, objective, update_membership
from src.data import load_paper_data, demo_initial_centers, membership_preset, ssmc_preset


@pytest.mark.parametrize('algorithm',ALGORITHMS)
def test_every_snapshot_is_consistent_and_objective_descends(algorithm):
    X,_=load_paper_data(); V=demo_initial_centers()
    c=Config(algorithm=algorithm,lambda_=0.1)
    B=membership_preset(0.3); t=np.array(ssmc_preset(8).targets)
    r=fit(X,c,V,B,t)
    np.testing.assert_array_equal(r.history[0].centers,V)
    assert len(r.history)==r.n_iter+1 and r.history[0].center_shift==0
    for i,s in enumerate(r.history):
        assert s.iteration==i
        np.testing.assert_allclose(s.membership,update_membership(X,s.centers,c,B,t),atol=1e-14)
        assert s.objective==pytest.approx(objective(X,s.membership,s.centers,c,B,t))
        if i:
            assert s.center_shift==pytest.approx(np.linalg.norm(s.centers-r.history[i-1].centers,axis=1).max())
    assert np.max(np.diff([s.objective for s in r.history]))<=1e-9
    assert r.stop_reason=='epsilon' and r.history[-1].center_shift<=c.epsilon
    np.testing.assert_array_equal(r.membership,r.history[-1].membership)
    r.membership[:]=0; r.centers[:]=0; V[:]=0
    assert r.history[-1].membership.sum()>0 and r.history[0].centers.sum()>0
    with pytest.raises(ValueError):
        r.history[0].membership[0,0]=0


def test_max_iter_history_includes_zero_and_final():
    r=fit(load_paper_data()[0],Config(max_iter=1),demo_initial_centers())
    assert [s.iteration for s in r.history]==[0,1]
    assert r.stop_reason=='max_iter' and r.history[-1].center_shift>r.config.epsilon
