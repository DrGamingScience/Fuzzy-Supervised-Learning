import numpy as np
import pytest
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score

from src.metrics import geometric_metrics
from src.metrics import pair_counts, external_metrics
from src.metrics import supervision_mask, metric_report
from sklearn.metrics import adjusted_rand_score


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


def test_pair_counts_by_hand_and_permutation():
    # 6 cặp: a=0, b=2, c=2, d=2.
    a=[0,0,1,1]; b=[0,1,0,1]
    assert pair_counts(a,b)==dict(a=0,b=2,c=2,d=2)
    r=external_metrics(a,b)
    assert r['ari'].value==pytest.approx(-0.5)
    assert r['jaccard'].value==0
    assert external_metrics(a,[8,9,8,9])==r
    assert external_metrics(a,[9,9,8,8])['jaccard'].value==1
    assert pair_counts([0,0,1,1],[0,0,0,1])==dict(a=1,b=1,c=2,d=2)
    assert external_metrics([0,0,1,1],[0,0,0,1])['jaccard'].value==0.25


@pytest.mark.parametrize('seed',range(5))
def test_ari_against_library_and_pairs_against_brute_force(seed):
    rng=np.random.default_rng(seed); a=rng.integers(0,4,23); b=rng.integers(0,3,23)
    counts=dict(a=0,b=0,c=0,d=0)
    for i in range(len(a)):
        for j in range(i+1,len(a)):
            name='a' if a[i]==a[j] and b[i]==b[j] else 'b' if a[i]==a[j] else 'c' if b[i]==b[j] else 'd'
            counts[name]+=1
    assert pair_counts(a,b)==counts
    assert external_metrics(a,b)['ari'].value==pytest.approx(adjusted_rand_score(a,b))


def test_degenerate_external_conventions():
    for labels in [[0,0,0],[0,1,2]]:
        r=external_metrics(labels,labels)
        assert r['ari'].value==r['jaccard'].value==1
    for labels in [[],[0]]:
        assert all(v.value is None and v.reason for v in external_metrics(labels,labels).values())


@pytest.mark.parametrize('algorithm',['fcm','ssfcm','ssfcm1','esfcm','ssmc'])
def test_report_full_and_unseen_masks(algorithm):
    X=np.arange(8,dtype=float).reshape(4,2); y=np.array([0,0,1,1]); predicted=[1,0,1,1]
    B=np.array([[0.3,0],[0,0],[0,0],[0,0]])
    mask=supervision_mask(algorithm,4,B=B,targets=np.array([0,-1,-1,-1]))
    assert mask.tolist()==([False]*4 if algorithm=='fcm' else [True,False,False,False])
    r=metric_report(X,predicted,y,mask)
    assert r['all']==external_metrics(y,predicted)
    assert r['unsupervised']==external_metrics(y[~mask],np.array(predicted)[~mask])


def test_missing_reference_and_too_few_unseen():
    X=np.array([[0.],[1.],[3.]])
    r=metric_report(X,[0,0,1])
    assert all(v.value is None and v.reason for v in r['all'].values())
    for mask in [np.array([True]*3),np.array([True,True,False])]:
        r=metric_report(X,[0,0,1],[0,0,1],mask)
        assert all(v.value is None and v.reason for v in r['unsupervised'].values())
    with pytest.raises(ValueError): metric_report(X,[0,0,1],supervised=[0,0,1])
