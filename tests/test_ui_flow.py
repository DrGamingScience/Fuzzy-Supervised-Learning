"""Nghiệm thu luồng thật trong script Streamlit bằng AppTest, không mock widget."""
import io
import json
from pathlib import Path
from unittest.mock import patch
import zipfile

import numpy as np
import pytest
from streamlit.testing.v1 import AppTest

from src.algorithms import fit

APP=str(Path(__file__).resolve().parents[1]/'app.py')


def edit(app,edited,rerun=True):
    key=f"supervision_editor_{app.session_state['editor_revision']}"
    app.session_state[key]={'edited_rows':edited,'added_rows':[],'deleted_rows':[]}
    if rerun: app.run()


@pytest.mark.parametrize('algorithm,expected',[
    ('fcm',0.188663),('ssfcm',0.451669),('ssfcm1',0.3),('esfcm',None),('ssmc',0.428699)])
def test_all_single_algorithms_through_ui(algorithm,expected):
    app=AppTest.from_file(APP).run()
    app.selectbox(key='algorithm').select(algorithm).run()
    app.button(key='run').click().run(timeout=20)
    assert not app.exception and not app.error
    r=app.session_state['experiment'].results[algorithm]
    if expected is not None: assert r.membership[8,0]==pytest.approx(expected,abs=1e-6)
    assert app.session_state['export_bytes'][:2]==b'PK'
    if algorithm=='esfcm': assert any('không khớp' in w.value for w in app.warning)


def test_preset_edit_run_view_compare_export_full_flow():
    with patch('src.experiments.fit',wraps=fit) as spy:
        app=AppTest.from_file(APP).run()
        app.selectbox(key='algorithm').select('ssfcm').run()
        app.selectbox(key='level').select(0.6).run()
        changes={0:{'membership':0.4},1:{'enabled':False}}
        # AppTest chưa có API data_editor; gửi delta cùng sự kiện chạy như frontend.
        edit(app,changes,rerun=False)
        app.button(key='run').click().run(timeout=20)
        assert spy.call_count==1 and not app.exception and not app.error
        exp=app.session_state['experiment']
        assert exp.B[8,0]==0.4 and exp.B[9,0]==0
        assert exp.targets[8]==0 and exp.targets[9]==-1
        app.slider[0].set_value(0).run()
        assert spy.call_count==1
        table=next(d.value for d in app.dataframe if 'U1' in d.value.columns)
        np.testing.assert_allclose(table[['U1','U2']],exp.results['ssfcm'].history[0].membership)
        app.radio(key='mode').set_value('So sánh cả năm').run()
        assert any('lần chạy trước' in w.value for w in app.warning)
        edit(app,changes,rerun=False)
        app.button(key='run').click().run(timeout=20)
        assert spy.call_count==6 and not app.exception
        exp=app.session_state['experiment']
        assert exp.B[8,0]==0.4 and exp.B[9,0]==0
        for a in exp.results:
            app.selectbox(key='result_algorithm').select(a).run()
            assert not app.exception
        assert spy.call_count==6
        with zipfile.ZipFile(io.BytesIO(app.session_state['export_bytes'])) as z:
            saved=json.loads(z.read('result.json'))
            assert len(saved['results'])==5 and saved['B'][8][0]==0.4
            assert saved['targets'][9] is None
            for a,r in exp.results.items():
                np.testing.assert_array_equal(saved['results'][a]['membership'],r.membership)
        assert len(app.get('download_button'))==1


def test_invalid_inputs_block_run_and_failed_config_preserves_result():
    app=AppTest.from_file(APP).run()
    app.selectbox(key='algorithm').select('ssfcm').run()
    app.button(key='run').click().run()
    saved=app.session_state['export_bytes']
    for changes,word in [({0:{'point_id':99}},'ID'),({0:{'membership':-1}},'B'),({0:{'point_id':10}},'trùng')]:
        edit(app,changes)
        assert any(word in e.value for e in app.error)
        assert app.button(key='run').disabled
        assert app.session_state['export_bytes']==saved
        app.button(key='reset_supervision').click().run()
    app.selectbox(key='algorithm').select('ssmc').run()
    app.number_input(key='m').set_value(5.0).run()
    app.button(key='run').click().run()
    assert any('M\'' in e.value for e in app.error)
    assert app.session_state['export_bytes']==saved and not app.exception
    app.number_input(key='m_prime').set_value(8.).run()
    app.button(key='run').click().run(timeout=20)
    assert not app.error and not app.exception


def test_b_preset_survives_algorithm_switch_and_zero_preset():
    app=AppTest.from_file(APP).run()
    app.selectbox(key='algorithm').select('ssfcm').run()
    app.selectbox(key='level').select(0.6).run()
    app.selectbox(key='algorithm').select('ssmc').run()
    app.selectbox(key='algorithm').select('ssfcm').run()
    assert app.selectbox(key='level').value==0.6
    app.selectbox(key='level').select(0.).run()
    app.button(key='run').click().run()
    assert app.session_state['experiment'].B.sum()==0 and not app.exception
    assert app.session_state['experiment'].results['ssfcm'].membership[8,0]==pytest.approx(0.188663,abs=1e-6)
