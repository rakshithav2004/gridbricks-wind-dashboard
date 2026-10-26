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
    rmse = sqrt(sum(error ** 2 for error in errors) / len(errors))
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
    """Match hourly forecasts to average actual generation for that hour."""

    actual_by_hour: dict[str, list[float]] = {}

    for record in actual_records:
        if str(record.get("fuelType", "")).upper() != "WIND":
            continue

        start_time = record.get("startTime")
        generation = record.get("generation")

        if start_time is None or generation is None:
            continue

        # Normalize the timestamp to its hour.
        hour = start_time[:13]

        actual_by_hour.setdefault(hour, []).append(float(generation))

    matched = []

    for record in forecast_records:
        start_time = record.get("startTime")
        generation = record.get("generation")

        if start_time is None or generation is None:
            continue

        hour = start_time[:13]
        actual_values = actual_by_hour.get(hour, [])

        # Only compare complete hours with two half-hour actual records.
        if len(actual_values) != 2:
            continue

        matched.append(
            {
                "startTime": start_time,
                "settlementDate": record.get("settlementDate"),
                "settlementPeriod": record.get("settlementPeriod"),
                "actual": round(sum(actual_values) / 2, 2),
                "forecast": float(generation),
                "publishTime": record.get("publishTime"),
            }
        )

    return sorted(matched, key=lambda item: item["startTime"])