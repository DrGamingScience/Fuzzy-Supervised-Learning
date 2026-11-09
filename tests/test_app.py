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
