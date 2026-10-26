from math import sqrt

def calculate_metrics(
    actual_values: list[float],
    forecast_values: list[float],
) -> dict:
    """Calculate forecast accuracy metrics for aligned values."""

    if len(actual_values) != len(forecast_values):
        raise ValueError(
            "Actual and forecast lists must have equal lengths."
        )

    if not actual_values:
        return {
            "count": 0,
            "mae": None,
            "rmse": None,
            "bias": None,
        }

    errors = [
        forecast - actual
        for actual, forecast in zip(actual_values, forecast_values)
    ]

    mae = sum(abs(error) for error in errors) / len(errors)

    rmse = sqrt(
        sum(error ** 2 for error in errors) / len(errors)
    )

    bias = sum(errors) / len(errors)

    return {
        "count": len(errors),
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "bias": round(bias, 2),
    }


def match_actual_and_forecast(
    actual_records: list[dict],
    forecast_records: list[dict],
) -> list[dict]:
    """Match actual and forecast records by date and settlement period."""

    actual_by_period = {
        (
            record["settlementDate"],
            record["settlementPeriod"],
        ): record
        for record in actual_records
        if record.get("fuelType") == "WIND"
    }

    forecast_by_period = {
        (
            record["settlementDate"],
            record["settlementPeriod"],
        ): record
        for record in forecast_records
    }

    common_periods = sorted(
        actual_by_period.keys() & forecast_by_period.keys()
    )

    return [
        {
            "settlementDate": date,
            "settlementPeriod": period,
            "actual": actual_by_period[(date, period)]["generation"],
            "forecast": forecast_by_period[(date, period)]["generation"],
        }
        for date, period in common_periods
    ]