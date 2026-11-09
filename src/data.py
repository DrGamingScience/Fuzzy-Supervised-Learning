"""Dữ liệu gốc và preset tái hiện; xem docs/DATA.md để đối chiếu nguồn.

Tọa độ: Endo et al. (2009), Table I, trang PDF 4 (trang in 1122);
Khang et al. (2021), Algorithms 14, 258, Table 1, trang 4.
Quy ước nội bộ: hàng điểm/cột cụm bắt đầu 0; ID hiển thị bắt đầu 1.
"""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


PAPER_POINT_IDS = tuple(range(1, 21))
MEMBERSHIP_LEVELS = (0.0, 0.3, 0.6)
SSMC_M_PRIME_VALUES = (2.0, 4.0, 8.0)

# Giữ nguyên thứ tự ID bài báo; không chuẩn hóa hoặc thêm nhãn vào X.
_COORDINATES = (
    (0.00, 4.50), (0.00, 5.50),
    (1.75, 4.50), (1.75, 5.50),
    (3.50, 4.50), (3.50, 5.50),
    (5.25, 4.50), (5.25, 5.50),
    (7.00, 4.50), (7.00, 5.50),
    (9.00, 0.00), (9.00, 2.50), (9.00, 5.00),
    (9.00, 7.50), (9.00, 10.00),
    (10.00, 0.00), (10.00, 2.50), (10.00, 5.00),
    (10.00, 7.50), (10.00, 10.00),
)


def load_paper_data() -> tuple[NDArray[np.float64], NDArray[np.int64]]:
    """Trả X (20, 2) và nhãn tham chiếu y (20,) thành hai bản sao riêng.

    y = 0 cho ID 1–10, y = 1 cho ID 11–20: nhóm tham chiếu của demo,
    không phải nhãn phân cụm được tính và không tự truyền vào thuật toán.
    """
    return np.array(_COORDINATES, dtype=np.float64), np.repeat([0, 1], 10).astype(np.int64)


def demo_initial_centers() -> NDArray[np.float64]:
    """Tâm đầu cố định của dự án: (2.7, 5), (9.1, 5); không lấy từ bài báo.

    Trả bản sao mới mỗi lần gọi; không cần seed vì không lấy mẫu ngẫu nhiên.
    Đây là tâm khởi tạo, không phải các tâm hội tụ trong bảng kết quả.
    """
    return np.array(((2.7, 5.0), (9.1, 5.0)), dtype=np.float64)


def membership_preset(level: float) -> NDArray[np.float64]:
    """B theo ba case ở mục III.A (2009) / mục 2.2 (2021).

    Chỉ ID 9, 10 → cụm hiển thị 1 có B = level; mọi ô khác bằng 0.
    B là chỉ dẫn giám sát, không phải U cuối và không phải hệ số M'.
    Hàm chỉ chọn preset; validation đầu vào thuật toán thuộc CORE-001.
    """
    if level not in MEMBERSHIP_LEVELS:
        raise ValueError("Preset độ thuộc chỉ nhận 0, 0.3 hoặc 0.6.")
    prior = np.zeros((20, 2), dtype=np.float64)
    prior[8:10, 0] = level
    return prior


@dataclass(frozen=True)
class SSMCPreset:
    """M, M' và cụm đích nội bộ; -1 = chưa giám sát, 0 = cụm hiển thị 1."""

    m: float
    m_prime: float
    targets: tuple[int, ...]


def ssmc_preset(m_prime: float) -> SSMCPreset:
    """Ba case ở mục 4 (2021): M = 2, M' = 2 / 4 / 8.

    M' = 2: không giám sát. M' = 4 hoặc 8: ID 9, 10 → cụm 1.
    Không tính ma trận số mũ hoặc cập nhật độ thuộc ở tầng dữ liệu này.
    """
    if m_prime not in SSMC_M_PRIME_VALUES:
        raise ValueError("Preset M' chỉ nhận 2, 4 hoặc 8.")
    targets = [-1] * 20
    if m_prime != 2:
        targets[8:10] = [0, 0]
    return SSMCPreset(m=2.0, m_prime=float(m_prime), targets=tuple(targets))
