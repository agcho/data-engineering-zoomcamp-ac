import requests
import dlt
from typing import Iterator, Dict, Any, Optional


BASE_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"
PAGE_SIZE = 1000


def fetch_page(page: int, timeout_s: int = 60) -> list[dict]:
    """
    Fetch one page from the custom API.
    Assumes the API supports `page` and `page_size` query params.
    Stops when API returns an empty list.

    If your API uses different param names (e.g., `limit`/`offset`),
    change params below.
    """
    params = {"page": page, "page_size": PAGE_SIZE}
    r = requests.get(BASE_URL, params=params, timeout=timeout_s)
    r.raise_for_status()
    data = r.json()

    # Expected: JSON array of trip records
    if isinstance(data, list):
        return data

    # Sometimes APIs wrap results in a dict (e.g., {"data": [...]}).
    # If that happens, adjust here.
    if isinstance(data, dict):
        for key in ("data", "results", "items"):
            if key in data and isinstance(data[key], list):
                return data[key]

    raise ValueError(f"Unexpected response format: {type(data)} -> {str(data)[:200]}")


@dlt.resource(name="yellow_taxi_trips", write_disposition="replace")
def yellow_taxi_trips() -> Iterator[Dict[str, Any]]:
    """
    Reads paginated taxi trip data:
    - 1000 records per page
    - stop when an empty page is returned
    """
    page = 1
    while True:
        rows = fetch_page(page)
        if not rows:
            break
        for row in rows:
            yield row
        page += 1


@dlt.source
def nyc_taxi_source():
    return yellow_taxi_trips()


def main() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="taxi_data",
    )

    load_info = pipeline.run(nyc_taxi_source())
    print(load_info)

    # Helpful: show where DuckDB file is
    print("\nDuckDB is stored at:", pipeline.destination)
    
if __name__ == "__main__":
    main()