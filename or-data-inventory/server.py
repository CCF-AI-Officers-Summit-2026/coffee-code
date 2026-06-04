from fastmcp import FastMCP
import httpx
import json

mcp = FastMCP("Oregon Agency Data Inventory")

API_BASE = "https://data.oregon.gov/resource/yp9j-pm7w.json"


@mcp.tool()
async def search_datasets(query: str, max_results: int = 10) -> str:
    """Search Oregon's statewide agency data inventory by keyword.

    Searches dataset names and descriptions across all state agencies.
    Returns matching datasets with their agency, description, classification,
    and publishing status.

    Args:
        query: What to search for (e.g., "water quality", "permits", "salary")
        max_results: Maximum number of results to return (default 10)
    """
    # Split query into individual terms so "environmental permits" matches
    # records containing both words, even if they're not adjacent.
    # Each term can match in the dataset name, description, OR agency name.
    terms = query.strip().split()
    term_conditions = []
    for term in terms:
        term_conditions.append(
            f"(lower(dataset_name) like lower('%{term}%') "
            f"OR lower(brief_description_of_data) like lower('%{term}%') "
            f"OR lower(agency_name) like lower('%{term}%'))"
        )
    where_clause = " AND ".join(term_conditions)

    async with httpx.AsyncClient() as client:
        resp = await client.get(API_BASE, params={
            "$where": where_clause,
            "$limit": max_results,
            "$order": "agency_name",
        }, timeout=30)
        resp.raise_for_status()
        data = resp.json()

    if not data:
        return f"No datasets found matching '{query}'."

    results = []
    for d in data:
        results.append({
            "inventory_id": d.get("inventory_id", ""),
            "agency": d.get("agency_name", ""),
            "dataset_name": d.get("dataset_name", ""),
            "description": d.get("brief_description_of_data", ""),
            "classification": d.get("data_classification", ""),
            "publishable": d.get("data_is_is_not_publishable", ""),
            "publishing_status": d.get("open_data_publishing_status", ""),
        })
    return json.dumps(results, indent=2)


@mcp.tool()
async def list_agencies() -> str:
    """List all Oregon state agencies in the data inventory with their dataset counts.

    Returns every agency and how many datasets they have inventoried,
    sorted by count (most datasets first).
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(API_BASE, params={
            "$select": "agency_name, count(*) as count",
            "$group": "agency_name",
            "$order": "count DESC",
            "$limit": 200,
        }, timeout=30)
        resp.raise_for_status()
        data = resp.json()

    results = []
    for d in data:
        results.append({
            "agency": d["agency_name"],
            "dataset_count": int(d["count"]),
        })
    return json.dumps(results, indent=2)


@mcp.tool()
async def get_agency_datasets(agency_name: str, max_results: int = 20) -> str:
    """Get all datasets for a specific Oregon state agency.

    Args:
        agency_name: Full or partial agency name (e.g., "Health Authority", "Transportation")
        max_results: Maximum number of results to return (default 20)
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(API_BASE, params={
            "$where": f"lower(agency_name) like lower('%{agency_name}%')",
            "$limit": max_results,
            "$order": "dataset_name",
        }, timeout=30)
        resp.raise_for_status()
        data = resp.json()

    if not data:
        return f"No datasets found for agency matching '{agency_name}'. Use list_agencies to see all agency names."

    results = []
    for d in data:
        results.append({
            "inventory_id": d.get("inventory_id", ""),
            "dataset_name": d.get("dataset_name", ""),
            "description": d.get("brief_description_of_data", ""),
            "classification": d.get("data_classification", ""),
            "contains_pii": d.get("data_contains_pii_phi", ""),
            "publishable": d.get("data_is_is_not_publishable", ""),
            "publishing_status": d.get("open_data_publishing_status", ""),
            "priority": d.get("overall_priority", ""),
        })
    return json.dumps(results, indent=2)


@mcp.tool()
async def get_dataset_details(inventory_id: str) -> str:
    """Get full details for a specific dataset by its inventory ID.

    Args:
        inventory_id: The inventory ID (e.g., "DELC-202410011749-00001")
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(API_BASE, params={
            "$where": f"inventory_id='{inventory_id}'",
            "$limit": 1,
        }, timeout=30)
        resp.raise_for_status()
        data = resp.json()

    if not data:
        return f"No dataset found with inventory ID '{inventory_id}'."

    return json.dumps(data[0], indent=2)


@mcp.tool()
async def filter_datasets(
    publishable: str = "",
    classification: str = "",
    contains_pii: str = "",
    priority: str = "",
    max_results: int = 20,
) -> str:
    """Filter Oregon datasets by classification, publishability, PII status, or priority.

    Use this to find datasets matching specific criteria, like all high-priority
    unpublished datasets or all datasets containing PII.

    Args:
        publishable: Filter by publishability (e.g., "Publishable as-is", "Requires redaction", "Not publishable")
        classification: Filter by data classification level (e.g., "Level 1", "Level 2", "Level 3", "Level 4")
        contains_pii: Filter by PII/PHI status (e.g., "Yes", "No")
        priority: Filter by overall priority (e.g., "High", "Medium", "Low")
        max_results: Maximum number of results to return (default 20)
    """
    conditions = []
    if publishable:
        conditions.append(f"lower(data_is_is_not_publishable) like lower('%{publishable}%')")
    if classification:
        conditions.append(f"lower(data_classification) like lower('%{classification}%')")
    if contains_pii:
        conditions.append(f"lower(data_contains_pii_phi) like lower('%{contains_pii}%')")
    if priority:
        conditions.append(f"lower(overall_priority) like lower('%{priority}%')")

    if not conditions:
        return "Please provide at least one filter: publishable, classification, contains_pii, or priority."

    where_clause = " AND ".join(conditions)

    async with httpx.AsyncClient() as client:
        resp = await client.get(API_BASE, params={
            "$where": where_clause,
            "$limit": max_results,
            "$order": "agency_name, dataset_name",
        }, timeout=30)
        resp.raise_for_status()
        data = resp.json()

    if not data:
        return f"No datasets found matching those filters."

    results = []
    for d in data:
        results.append({
            "inventory_id": d.get("inventory_id", ""),
            "agency": d.get("agency_name", ""),
            "dataset_name": d.get("dataset_name", ""),
            "classification": d.get("data_classification", ""),
            "contains_pii": d.get("data_contains_pii_phi", ""),
            "publishable": d.get("data_is_is_not_publishable", ""),
            "priority": d.get("overall_priority", ""),
        })
    return json.dumps(results, indent=2)


if __name__ == "__main__":
    mcp.run()
