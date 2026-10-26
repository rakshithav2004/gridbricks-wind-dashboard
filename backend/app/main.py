from datetime import date
import httpx
from fastapi import FastAPI, HTTPException, Query

from app.analysis import calculate_metrics, match_actual_and_forecast
from app.elexon import fetch_dataset, fetch_wind_forecast

app = FastAPI(
    title="Gridbricks Wind Forecast API",
    description="UK wind generation and forecast analysis.",
    version="0.2.0",
)


@app.get("/")
def root():
    return {
        "message": "Gridbricks Wind Forecast API is running",
        "status": "ok",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


def validate_dates(start: date, end: date):
    if end <= start:
        raise HTTPException(
            status_code=400,
            detail="'end' must be later than 'start'.",
        )


async def load_actual_wind(start: date, end: date) -> list:
    records = await fetch_dataset(
        "FUELHH",
        f"{start.isoformat()}T00:00:00Z",
        f"{end.isoformat()}T00:00:00Z",
    )

    return [
        record
        for record in records
        if str(record.get("fuelType", "")).upper() == "WIND"
    ]


async def load_forecasts(start: date, end: date) -> list:
    return await fetch_wind_forecast(
        f"{start.isoformat()}T00:00:00Z",
        f"{end.isoformat()}T00:00:00Z",
    )


@app.get("/api/wind/actual")
async def get_actual_generation(
    start: date = Query(default=date(2026, 1, 1)),
    end: date = Query(default=date(2026, 1, 2)),
):
    validate_dates(start, end)

    try:
        records = await load_actual_wind(start, end)
        return {
            "dataset": "FUELHH",
            "start": start.isoformat(),
            "end": end.isoformat(),
            "count": len(records),
            "data": records,
        }
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve actual generation data from Elexon.",
        ) from exc
    except ValueError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/api/wind/forecast")
async def get_wind_forecast(
    start: date = Query(default=date(2026, 1, 1)),
    end: date = Query(default=date(2026, 1, 2)),
):
    validate_dates(start, end)

    try:
        records = await load_forecasts(start, end)
        return {
            "dataset": "WINDFOR",
            "start": start.isoformat(),
            "end": end.isoformat(),
            "count": len(records),
            "data": records,
        }
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve wind forecast data from Elexon.",
        ) from exc
    except ValueError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/api/wind/analysis")
async def get_wind_analysis(
    start: date = Query(default=date(2026, 1, 1)),
    end: date = Query(default=date(2026, 1, 2)),
):
    validate_dates(start, end)

    try:
        actual_records = await load_actual_wind(start, end)
        forecast_records = await load_forecasts(start, end)

        matched = match_actual_and_forecast(
            actual_records,
            forecast_records,
        )

        metrics = calculate_metrics(
            [float(record["actual"]) for record in matched],
            [float(record["forecast"]) for record in matched],
        )

        return {
            "start": start.isoformat(),
            "end": end.isoformat(),
            "actual_count": len(actual_records),
            "forecast_count": len(forecast_records),
            "matched_count": len(matched),
            "metrics": metrics,
            "data": matched,
        }

    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve wind data from Elexon.",
        ) from exc
    except ValueError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc