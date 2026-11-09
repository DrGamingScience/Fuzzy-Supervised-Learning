"""Chạy thật script Streamlit bằng AppTest."""

from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_entry_point_renders_demo_without_exception():
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"))
    app.run(timeout=15)
    assert not app.exception
    assert app.title[0].value == "Phân cụm mờ bán giám sát"
    table=app.dataframe[0].value
    assert len(table)==20
    assert list(table['ID điểm'])==list(range(1,21))
    assert set(table['Nhóm tham chiếu'])=={'Nhóm 1','Nhóm 2'}
    assert table.loc[8,'x']==7


def test_algorithm_controls_and_presets():
    app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py')).run()
    assert app.selectbox(key='algorithm').options==['FCM','sSFCM (m > 1)','sSFCM (m = 1)','eSFCM','sSMC-FCM']
    app.selectbox(key='algorithm').select('ssfcm').run()
    assert app.selectbox(key='level').value==0.3
    app.selectbox(key='level').select(0.6).run()
    assert app.selectbox(key='level').value==0.6
    app.selectbox(key='algorithm').select('ssmc').run()
    app.selectbox(key='m_prime_preset').select(8.0).run()
    assert app.number_input(key='m_prime').value==8.0
    app.selectbox(key='algorithm').select('esfcm').run()
    assert app.number_input(key='lambda').value==1.0
    assert 'm' not in [w.key for w in app.number_input]
    app.selectbox(key='algorithm').select('ssfcm1').run()
    assert not app.exception
