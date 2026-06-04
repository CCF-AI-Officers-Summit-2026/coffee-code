from typing import Any

from fastmcp import FastMCP
import httpx


DATASET_ID = "cnih-y5dw"
DATASET_API_URL = f"https://health.data.ny.gov/resource/{DATASET_ID}.json"
DATASET_PAGE_URL = (
    "https://health.data.ny.gov/Health/"
    "Food-Service-Establishment-Last-Inspection/cnih-y5dw/about_data"
)

RESULT_COLUMNS = [
    "facility",
    "address",
    "date",
    "violations",
    "total_critical_violations",
    "total_crit_not_corrected",
    "total_noncritical_violations",
    "description",
    "local_health_department",
    "county",
    "city",
    "inspection_type",
    "inspection_comments",
    "nys_health_operation_id",
]

mcp = FastMCP("NY Food Service Inspection Server")


def _quote_soql_text(value: str) -> str:
    """Quote a string value for a simple SoQL where clause."""
    return value.replace("'", "''")


def _clamp_max_results(max_results: int) -> int:
    return max(1, min(max_results, 25))


def _format_date(raw_date: str | None) -> str:
    if not raw_date:
        return "Unknown"
    return raw_date.split("T", maxsplit=1)[0]


def _format_record(record: dict[str, Any], index: int) -> str:
    facility = record.get("facility", "Unknown facility")
    address = record.get("address", "Unknown address")
    city = record.get("city", "Unknown city")
    county = record.get("county", "Unknown county")
    inspection_date = _format_date(record.get("date"))
    critical = record.get("total_critical_violations", "Unknown")
    critical_not_corrected = record.get("total_crit_not_corrected", "Unknown")
    noncritical = record.get("total_noncritical_violations", "Unknown")
    violations = record.get("violations", "No violation text provided.")
    operation_id = record.get("nys_health_operation_id", "Unknown")

    return (
        f"{index}. {facility}\n"
        f"   Address: {address}\n"
        f"   City/County: {city}, {county} County\n"
        f"   Last inspected: {inspection_date}\n"
        f"   Violations: {violations}\n"
        f"   Critical violations: {critical}; "
        f"critical not corrected: {critical_not_corrected}; "
        f"noncritical: {noncritical}\n"
        f"   NYS health operation ID: {operation_id}"
    )


@mcp.tool()
async def search_food_inspections(
    query: str | None = None,
    city: str | None = None,
    county: str | None = None,
    min_critical_violations: int = 0,
    max_results: int = 10,
) -> str:
    """Search NY food service establishment last-inspection records.

    Use this for questions about restaurants, cafeterias, snack bars, and other
    food service establishments in New York State. The tool searches the latest
    inspection record in the NY Department of Health dataset.

    Args:
        query: Optional text to search, such as a facility name or violation.
        city: Optional city filter, such as "Albany" or "Rochester".
        county: Optional county filter, such as "Albany" or "Monroe".
        min_critical_violations: Only return records with at least this many
            critical violations.
        max_results: Maximum number of records to return, from 1 to 25.
    """
    limit = _clamp_max_results(max_results)
    where_clauses = []

    if city:
        where_clauses.append(f"city = '{_quote_soql_text(city.upper())}'")
    if county:
        where_clauses.append(f"county = '{_quote_soql_text(county.upper())}'")
    if min_critical_violations > 0:
        where_clauses.append(
            f"total_critical_violations >= {min_critical_violations}"
        )

    params: dict[str, str | int] = {
        "$select": ",".join(RESULT_COLUMNS),
        "$order": "date DESC",
        "$limit": limit,
    }
    if query:
        params["$q"] = query
    if where_clauses:
        params["$where"] = " AND ".join(where_clauses)

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(DATASET_API_URL, params=params)
        response.raise_for_status()
        records = response.json()

    if not records:
        return (
            "No matching inspection records were found. Try a broader search, "
            "or remove one of the city, county, or critical-violation filters.\n\n"
            f"Source: {DATASET_PAGE_URL}"
        )

    formatted_records = [
        _format_record(record, index)
        for index, record in enumerate(records, start=1)
    ]
    filters = []
    if query:
        filters.append(f'query="{query}"')
    if city:
        filters.append(f'city="{city}"')
    if county:
        filters.append(f'county="{county}"')
    if min_critical_violations > 0:
        filters.append(f"min_critical_violations={min_critical_violations}")

    filter_summary = ", ".join(filters) if filters else "no filters"

    return (
        "NY food service establishment last-inspection results\n"
        f"Filters: {filter_summary}\n"
        f"Returned: {len(records)} record(s)\n\n"
        + "\n\n".join(formatted_records)
        + "\n\n"
        f"Source: {DATASET_PAGE_URL}\n"
        "Note: This dataset reports each establishment's most recently "
        "reported inspection and is for reporting purposes only."
    )


if __name__ == "__main__":
    mcp.run()
