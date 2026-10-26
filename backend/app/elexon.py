import httpx

BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1"

async def fetch_dataset(
    dataset: str,
    start: str,
    end: str,
) -> list:
    """Fetch a raw Elexon dataset using publication-time filters."""

    url = f"{BASE_URL}/datasets/{dataset}/stream"

    params = {
        "publishDateTimeFrom": start,
        "publishDateTimeTo": end,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        result = response.json()

    if isinstance(result, list):
        return result

    if isinstance(result, dict):
        data = result.get("data", [])
        if isinstance(data, list):
            return data

    raise ValueError(
        f"Unexpected response format from Elexon dataset {dataset}"
    )


async def fetch_wind_forecast(
    start: str,
    end: str,
) -> list:
    """Fetch the latest historical view of wind forecasts."""

    url = f"{BASE_URL}/forecast/generation/wind/latest/stream"

    params = {
        "from": start,
        "to": end,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        result = response.json()

    if isinstance(result, list):
        return result

    if isinstance(result, dict):
        data = result.get("data", [])
        if isinstance(data, list):
            return data

    raise ValueError("Unexpected response format from Elexon wind forecast")