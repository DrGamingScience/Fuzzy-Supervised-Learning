import numpy as np
import pandas as pd
import pytest

from src.algorithms import ALGORITHMS, Config, fit
from src.data import load_paper_data, demo_initial_centers
from src.experiments import supervision_from_rows, run_experiment, comparison_table


def row(**changes):
    return dict(dict(enabled=True,point_id=9,target_cluster=1,membership=0.3),**changes)


@pytest.mark.parametrize('changes',[
    dict(point_id=0),dict(point_id=21),dict(point_id=9.5),dict(target_cluster=0),
    dict(target_cluster=3),dict(membership=-0.1),dict(membership=1.1),dict(membership=np.nan),dict(enabled='yes')])
def test_invalid_supervision(changes):
    with pytest.raises(ValueError): supervision_from_rows([row(**changes)],20,2)


def test_disabled_duplicate_and_membership_independence():
    B,t=supervision_from_rows(pd.DataFrame([row(),row(enabled=False,point_id=0,membership=np.nan)]),20,2)
    assert B[8,0]==0.3 and t[8]==0 and B.sum()==0.3
    with pytest.raises(ValueError,match='trùng'): supervision_from_rows([row(),row()],20,2)
    B,t=supervision_from_rows([row(membership='unused')],20,2,use_membership=False)
    assert B.sum()==0 and t[8]==0
    B,t=supervision_from_rows([row(membership=0)],20,2)
    assert B.sum()==0 and t[8]==0


def test_comparison_uses_same_data_initialization_and_revealed_information():
    X,y=load_paper_data(); V=demo_initial_centers()
    B,t=supervision_from_rows([row(),row(point_id=10)],20,2)
    configs=[Config(algorithm=a) for a in ALGORITHMS]
    exp=run_experiment(X,configs,V,B,t,y)
    for a,r in exp.results.items():
        np.testing.assert_array_equal(r.history[0].centers,V)
        np.testing.assert_array_equal(r.membership,fit(X,r.config,V,B,t).membership)
        assert exp.X.shape==(20,2)  # Không nối y vào X.
    X[:]=0; V[:]=0; B[:]=0; t[:]=-1; y[:]=99
    assert exp.X.sum()>0 and exp.initial_centers.sum()>0 and exp.B.sum()==0.6
    assert exp.reference.max()==1
    table=comparison_table(exp)
    assert len(table)==5 and 'objective' not in table and 'J' not in table
    assert table['parameters'].iloc[0]['seed']==42
    assert 'unsupervised.ari' in table


def test_random_initialization_is_shared():
    X,_=load_paper_data()
    exp=run_experiment(X,[Config(seed=1),Config(algorithm='ssfcm',seed=99)])
    np.testing.assert_array_equal(exp.results['fcm'].history[0].centers,exp.results['ssfcm'].history[0].centers)
