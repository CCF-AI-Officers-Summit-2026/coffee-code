# Oregon Agency Data Inventory — MCP Server

An MCP server that lets AI assistants search Oregon's statewide agency data inventory. Covers 7,000+ datasets across 66 state agencies, cataloged under HB 3361 (2017).

## Data Source

[State of Oregon Agency Data Inventory](https://data.oregon.gov/Administrative/State-of-Oregon-Agency-Data-Inventory/yp9j-pm7w) — A Socrata dataset maintained by Oregon's Chief Data Officer. Queries hit the live API, so results are always current.

## Setup

```bash
cd or-data-inventory
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python server.py
```

## Tools

| Tool | Description |
|---|---|
| `search_datasets(query)` | Search dataset names and descriptions by keyword |
| `list_agencies` | List all agencies with their dataset counts |
| `get_agency_datasets(agency_name)` | Get all datasets for a specific agency |
| `get_dataset_details(inventory_id)` | Get full details on a specific dataset |
| `filter_datasets(...)` | Filter by classification, PII status, publishability, or priority |

## Example Queries

- "Find datasets related to water quality"
- "Which agencies have the most data?"
- "What data does the Department of Environmental Quality have?"
- "Show me high-priority datasets that contain PII"
- "What datasets are publishable as-is but haven't been published yet?"
