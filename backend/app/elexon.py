import httpx

BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1/datasets"


async def fetch_dataset(
    dataset: str,
    start: str,
    end: str,
) -> list:
    """Fetch a dataset for a specified time range from Elexon."""

    url = f"{BASE_URL}/{dataset}/stream"

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

    raise ValueError(f"Unexpected response format from Elexon dataset {dataset}")