import numpy as np
import pytest
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

from src.metrics import geometric_metrics


def test_geometric_metrics_against_library_and_hand_count():
    X=np.array([[0.],[2.],[8.],[10.]])
    y=np.array([0,0,1,1]); r=geometric_metrics(X,y)
    assert r['silhouette'].value==pytest.approx((7/9+5/7)/2)
    assert r['ch'].value==pytest.approx(32)
    assert r['db'].value==pytest.approx(0.25)
    assert r['dunn'].value==pytest.approx(3)
    # E1=5+3+3+5=16, Ek=1+1+1+1=4, Dk=8, k=2.
    assert r['pbm'].value==pytest.approx(((16/4)*8/2)**2)
    assert r['db'].direction=='min'


@pytest.mark.parametrize('seed',[0,1,2])
def test_geometric_reference_random_data(seed):
    rng=np.random.default_rng(seed); X=rng.normal(size=(30,3)); y=np.repeat([7,19,33],10)
    r=geometric_metrics(X,y)
    assert r['silhouette'].value==pytest.approx(silhouette_score(X,y))
    assert r['ch'].value==pytest.approx(calinski_harabasz_score(X,y))
    assert r['db'].value==pytest.approx(davies_bouldin_score(X,y))


def test_singletons_and_undefined_partitions():
    X=np.array([[0.],[1.],[9.]])
    r=geometric_metrics(X,[0,0,1])
    assert r['silhouette'].value==pytest.approx(silhouette_score(X,[0,0,1]))
    for labels in [[1,1,1],[0,1,2]]:
        assert all(v.value is None and v.reason for v in geometric_metrics(X,labels).values())
    zero=geometric_metrics(np.zeros((4,2)),[0,0,1,1])
    for name in ['ch','db','dunn','pbm']:
        assert zero[name].value is None and zero[name].reason
    assert zero['silhouette'].value==0


def test_geometric_validation():
    with pytest.raises(ValueError): geometric_metrics([[0],[1]], [0])
    with pytest.raises(ValueError): geometric_metrics([[0],[np.nan]], [0,1])
