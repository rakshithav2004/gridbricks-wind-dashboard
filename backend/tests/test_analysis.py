import pytest
from app.analysis import calculate_metrics, match_actual_and_forecast

def test_calculate_metrics():
    result = calculate_metrics(
        [100, 200, 300],
        [110, 180, 330],
    )

    assert result["count"] == 3
    assert result["mae"] == 20.0
    assert result["rmse"] == 21.6
    assert result["bias"] == 6.67


def test_empty_values():
    result = calculate_metrics([], [])

    assert result == {
        "count": 0,
        "mae": None,
        "rmse": None,
        "bias": None,
    }


def test_mismatched_lengths():
    with pytest.raises(ValueError):
        calculate_metrics([100, 200], [110])


def test_match_actual_and_forecast_by_hour():
    actual_records = [
        {
            "startTime": "2026-01-01T00:00:00Z",
            "settlementDate": "2026-01-01",
            "settlementPeriod": 1,
            "fuelType": "WIND",
            "generation": 15000,
        },
        {
            "startTime": "2026-01-01T00:30:00Z",
            "settlementDate": "2026-01-01",
            "settlementPeriod": 2,
            "fuelType": "WIND",
            "generation": 15200,
        },
    ]

    forecast_records = [
        {
            "startTime": "2026-01-01T00:00:00Z",
            "settlementDate": "2026-01-01",
            "settlementPeriod": 1,
            "generation": 14800,
            "publishTime": "2025-12-31T22:30:00Z",
        },
    ]

    result = match_actual_and_forecast(actual_records, forecast_records)

    assert len(result) == 1
    assert result[0]["actual"] == 15100.0
    assert result[0]["forecast"] == 14800.0
    assert result[0]["startTime"] == "2026-01-01T00:00:00Z"


def test_match_ignores_non_wind_actual_records():
    actual_records = [
        {
            "startTime": "2026-01-01T00:00:00Z",
            "settlementDate": "2026-01-01",
            "settlementPeriod": 1,
            "fuelType": "WIND",
            "generation": 15000,
        },
        {
            "startTime": "2026-01-01T00:30:00Z",
            "settlementDate": "2026-01-01",
            "settlementPeriod": 2,
            "fuelType": "WIND",
            "generation": 15200,
        },
        {
            "startTime": "2026-01-01T00:00:00Z",
            "settlementDate": "2026-01-01",
            "settlementPeriod": 1,
            "fuelType": "GAS",
            "generation": 5000,
        },
    ]

    forecast_records = [
        {
            "startTime": "2026-01-01T00:00:00Z",
            "settlementDate": "2026-01-01",
            "settlementPeriod": 1,
            "generation": 14800,
        },
    ]

    result = match_actual_and_forecast(actual_records, forecast_records)

    assert len(result) == 1
    assert result[0]["actual"] == 15100.0