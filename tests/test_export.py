import io
import json
import zipfile

import numpy as np
import pandas as pd

from src.algorithms import ALGORITHMS, Config
from src.data import load_paper_data, demo_initial_centers, membership_preset, ssmc_preset
from src.experiments import run_experiment, export_zip


def test_zip_roundtrip_all_arrays_config_metrics_and_history():
    X,y=load_paper_data(); B=membership_preset(0.3); t=np.array(ssmc_preset(4).targets)
    exp=run_experiment(X,[Config(algorithm=a) for a in ALGORITHMS],demo_initial_centers(),B,t,y)
    with zipfile.ZipFile(io.BytesIO(export_zip(exp))) as z:
        raw=z.read('result.json').decode('utf-8')
        p=json.loads(raw,parse_constant=lambda s: (_ for _ in ()).throw(AssertionError(s)))
        np.testing.assert_array_equal(p['X'],X)
        np.testing.assert_array_equal(p['B'],B)
        assert p['targets'][8:10]==[1,1] and p['targets'][0] is None
        assert p['reference']==y.tolist()
        assert 'giám sát' in z.read('HUONG_DAN.txt').decode('utf-8-sig')
        df=pd.read_csv(io.BytesIO(z.read('data.csv')),encoding='utf-8-sig')
        np.testing.assert_array_equal(df[['x1','x2']],X)
        sup=pd.read_csv(io.BytesIO(z.read('supervision.csv')),encoding='utf-8-sig')
        np.testing.assert_array_equal(sup[['B1','B2']],B)
        for name,result in exp.results.items():
            saved=p['results'][name]
            assert saved['config']['algorithm']==name
            assert saved['n_iter']==result.n_iter and saved['stop_reason']==result.stop_reason
            assert saved['warnings']==list(result.warnings)
            np.testing.assert_array_equal(saved['membership'],result.membership)
            np.testing.assert_array_equal(saved['centers'],result.centers)
            np.testing.assert_array_equal(saved['labels'],result.labels+1)
            members=pd.read_csv(io.BytesIO(z.read(f'{name}/memberships.csv')))
            centers=pd.read_csv(io.BytesIO(z.read(f'{name}/centers.csv')))
            for snap,original in zip(saved['history'],result.history,strict=True):
                np.testing.assert_array_equal(snap['membership'],original.membership)
                np.testing.assert_array_equal(snap['centers'],original.centers)
                assert snap['objective']==original.objective
                np.testing.assert_allclose(members[members.iteration==original.iteration][['U1','U2']],original.membership,atol=1e-15)
                np.testing.assert_allclose(centers[centers.iteration==original.iteration][['x1','x2']],original.centers,atol=1e-14)
            for scope,metrics in exp.reports[name].items():
                for metric,value in metrics.items():
                    assert saved['metrics'][scope][metric]['value']==value.value


def test_export_undefined_metrics_as_null():
    X=np.zeros((4,2))
    exp=run_experiment(X,[Config()],initial_centers=X[:2])
    with zipfile.ZipFile(io.BytesIO(export_zip(exp))) as z:
        p=json.loads(z.read('result.json'))
        assert p['reference'] is None
        assert p['results']['fcm']['metrics']['geometric']['ch']['value'] is None
        assert p['results']['fcm']['metrics']['all']['ari']['reason']
