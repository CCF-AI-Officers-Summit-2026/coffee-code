from fastmcp import FastMCP
import httpx

# STEP 1: Name your server — this shows up when AI tools connect to it
mcp = FastMCP("My State Data Server")


# STEP 2: Define tools that fetch and return public data.
# Each tool becomes a capability the AI agent can call.
# Replace this example with your real data source.

@mcp.tool()
async def search_records(query: str, max_results: int = 10) -> str:
    """Search public records by keyword.

    Args:
        query: Search term (e.g., "road construction", "health department")
        max_results: Maximum number of results to return (default 10)
    """
    # Replace this URL and params with your actual data source
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://your-api-endpoint.gov/api/search",
            params={"q": query, "limit": max_results},
        )
        response.raise_for_status()
        return response.text


@mcp.tool()
async def get_record_details(record_id: str) -> str:
    """Get full details for a specific record by its ID.

    Args:
        record_id: The unique identifier of the record
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://your-api-endpoint.gov/api/records/{record_id}",
        )
        response.raise_for_status()
        return response.text


if __name__ == "__main__":
    mcp.run()
