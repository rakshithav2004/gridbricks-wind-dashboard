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

from app.analysis import match_actual_and_forecast


def test_match_actual_and_forecast_by_settlement_period():
    actual_records = [
        {
            "settlementDate": "2026-01-01",
            "settlementPeriod": 1,
            "fuelType": "WIND",
            "generation": 15000,
        },
        {
            "settlementDate": "2026-01-01",
            "settlementPeriod": 2,
            "fuelType": "WIND",
            "generation": 15200,
        },
    ]

    forecast_records = [
        {
            "settlementDate": "2026-01-01",
            "settlementPeriod": 1,
            "generation": 14800,
        },
    ]

    result = match_actual_and_forecast(actual_records, forecast_records)

    assert len(result) == 1
    assert result[0]["settlementPeriod"] == 1
    assert result[0]["actual"] == 15000
    assert result[0]["forecast"] == 14800


def test_match_ignores_non_wind_actual_records():
    actual_records = [
        {
            "settlementDate": "2026-01-01",
            "settlementPeriod": 1,
            "fuelType": "BIOMASS",
            "generation": 1000,
        },
    ]

    forecast_records = [
        {
            "settlementDate": "2026-01-01",
            "settlementPeriod": 1,
            "generation": 900,
        },
    ]

    result = match_actual_and_forecast(actual_records, forecast_records)

    assert result == []