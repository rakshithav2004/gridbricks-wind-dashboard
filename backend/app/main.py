from datetime import date

from fastapi import FastAPI, HTTPException, Query

from app.elexon import fetch_dataset

app = FastAPI(
    title="Gridbricks Wind Forecast API",
    description="UK wind generation and forecast analysis.",
    version="0.1.0",
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


@app.get("/api/wind/actual")
async def get_actual_generation(
    start: date = Query(default=date(2026, 1, 1)),
    end: date = Query(default=date(2026, 1, 2)),
):
    if end <= start:
        raise HTTPException(
            status_code=400,
            detail="'end' must be later than 'start'.",
        )

    try:
        records = await fetch_dataset(
            "FUELHH",
            f"{start.isoformat()}T00:00Z",
            f"{end.isoformat()}T00:00Z",
        )

        wind_records = [
            record
            for record in records
            if str(record.get("fuelType", "")).upper() == "WIND"
        ]

        return {
            "dataset": "FUELHH",
            "start": start.isoformat(),
            "end": end.isoformat(),
            "count": len(wind_records),
            "data": wind_records,
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
    if end <= start:
        raise HTTPException(
            status_code=400,
            detail="'end' must be later than 'start'.",
        )

    try:
        records = await fetch_dataset(
            "WINDFOR",
            f"{start.isoformat()}T00:00Z",
            f"{end.isoformat()}T00:00Z",
        )

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