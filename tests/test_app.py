"""Chạy thật script Streamlit bằng AppTest, không thực hiện clustering."""

from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_minimal_entry_point_renders_without_exception():
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"))
    app.run(timeout=15)
    assert not app.exception
    assert app.title[0].value == "Phân cụm mờ bán giám sát"
    assert app.success[0].value == "Môi trường đã sẵn sàng."
