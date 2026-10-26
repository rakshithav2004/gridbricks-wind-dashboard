from math import sqrt

def calculate_metrics(actual_values: list[float], forecast_values: list[float]) -> dict:
    """Calculate forecast accuracy metrics for aligned actual and forecast values."""

    if len(actual_values) != len(forecast_values):
        raise ValueError("Actual and forecast lists must have equal lengths.")

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
        sum(error**2 for error in errors) / len(errors)
    )

    bias = sum(errors) / len(errors)

    return {
        "count": len(errors),
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "bias": round(bias, 2),
    }