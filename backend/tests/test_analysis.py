import pytest
from app.analysis import calculate_metrics

def test_calculate_metrics():
    result = calculate_metrics(
        actual_values=[100, 200, 300],
        forecast_values=[110, 180, 330],
    )
    assert result["count"] == 3
    assert result["mae"] == 20.0
    assert result["rmse"] == 21.6
    assert result["bias"] == 6.67


def test_empty_values():
    result = calculate_metrics([], [])
    assert result["count"] == 0
    assert result["mae"] is None


def test_mismatched_lengths():
    with pytest.raises(ValueError):
        calculate_metrics([100, 200], [110])