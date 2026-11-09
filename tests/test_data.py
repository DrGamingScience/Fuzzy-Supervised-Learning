"""Kiểm tra toàn bộ bảng nguồn, tách nhãn và chỉ dẫn giám sát được tiết lộ."""

import csv
from dataclasses import FrozenInstanceError
from pathlib import Path

import numpy as np
import pytest

from src.data import (
    PAPER_POINT_IDS,
    demo_initial_centers,
    load_paper_data,
    membership_preset,
    ssmc_preset,
)


def test_all_coordinates_and_reference_groups_match_source_fixture():
    # Fixture được chép/đối chiếu hai bảng PDF, không sinh từ src/data.py.
    with (Path(__file__).parent / "fixtures/paper_20_points.csv").open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))
    x, y = load_paper_data()
    expected_x = [[float(row["x1"]), float(row["x2"])] for row in rows]
    expected_y = [int(row["reference_group"]) - 1 for row in rows]
    assert tuple(int(row["point_id"]) for row in rows) == PAPER_POINT_IDS == tuple(range(1, 21))
    np.testing.assert_array_equal(x, expected_x)
    np.testing.assert_array_equal(y, expected_y)
    assert x.shape == (20, 2) and y.shape == (20,)
    assert x.dtype == np.float64 and y.dtype == np.int64
    assert np.isfinite(x).all()
    assert not np.shares_memory(x, y)
    np.testing.assert_array_equal(np.bincount(y), [10, 10])


def test_data_and_centers_are_reproducible_and_independent_between_calls():
    x, y = load_paper_data()
    centers = demo_initial_centers()
    x[:] = -999
    y[:] = -999
    centers[:] = -999
    next_x, next_y = load_paper_data()
    assert next_x[0].tolist() == [0.0, 4.5]
    assert next_y.tolist() == [0] * 10 + [1] * 10
    np.testing.assert_array_equal(demo_initial_centers(), [[2.7, 5.0], [9.1, 5.0]])


@pytest.mark.parametrize("level", [0.0, 0.3, 0.6])
def test_membership_presets_only_reveal_paper_points_9_and_10(level):
    b = membership_preset(level)
    assert b.shape == (20, 2)
    assert b[8, 0] == b[9, 0] == level
    assert np.count_nonzero(b) == (0 if level == 0 else 2)
    assert np.all(b[:, 1] == 0)
    assert np.all((0 <= b.sum(axis=1)) & (b.sum(axis=1) <= 1))
    b[:] = -999
    assert membership_preset(level)[8, 0] == level


@pytest.mark.parametrize("m_prime", [2, 4, 8])
def test_ssmc_presets_keep_exponents_separate_from_membership(m_prime):
    preset = ssmc_preset(m_prime)
    assert preset.m == 2 and preset.m_prime == m_prime
    assert len(preset.targets) == 20
    supervised = [(i + 1, k + 1) for i, k in enumerate(preset.targets) if k != -1]
    assert supervised == ([] if m_prime == 2 else [(9, 1), (10, 1)])
    with pytest.raises(FrozenInstanceError):
        preset.m_prime = 99


@pytest.mark.parametrize("level", [-1, 0.2, 1, float("nan"), float("inf")])
def test_unknown_membership_preset_is_rejected(level):
    with pytest.raises(ValueError, match="Preset"):
        membership_preset(level)


@pytest.mark.parametrize("m_prime", [0, 3, 6, float("nan"), float("inf")])
def test_unknown_ssmc_preset_is_rejected(m_prime):
    with pytest.raises(ValueError, match="Preset"):
        ssmc_preset(m_prime)
