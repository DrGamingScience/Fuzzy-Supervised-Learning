"""Smoke test dependency, độc lập với dữ liệu và thuật toán dự án."""

import importlib
import json

import pytest


@pytest.mark.parametrize(
    "name", ["numpy", "scipy", "pandas", "sklearn", "streamlit", "plotly", "pytest"]
)
def test_runtime_imports(name):
    module = importlib.import_module(name)
    assert module.__version__


def test_numeric_table_and_chart_dependencies_work_together():
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go
    from scipy.linalg import norm

    # Kiểm tra một phép tính và đường dữ liệu → bảng → biểu đồ cục bộ.
    values = np.array([3.0, 4.0])
    assert norm(values) == pytest.approx(5.0)
    table = pd.DataFrame({"value": values})
    chart = go.Figure(go.Scatter(y=table["value"].tolist()))
    assert json.loads(chart.to_json())["data"][0]["y"] == [3.0, 4.0]
