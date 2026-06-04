# NY Food Service Inspection MCP Server

This project builds a small MCP server for the New York State Department of
Health dataset, **Food Service Establishment: Last Inspection**.

Dataset page:
https://health.data.ny.gov/Health/Food-Service-Establishment-Last-Inspection/cnih-y5dw/about_data

API endpoint:
https://health.data.ny.gov/resource/cnih-y5dw.json

## Why This Is Useful

The dataset includes the latest reported inspection for restaurants, school
cafeterias, snack bars, and other food service establishments in New York
State. An AI agent can use this MCP server to answer plain-English questions
like:

- Which Albany restaurants had critical violations in their most recent
  inspection?
- Find recent inspection records for Dunkin in Monroe County.
- Search for establishments with rodent-related violation text.

## Install

From this folder:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

If your virtual environment is not already active, activate it first:

```bash
source .venv/bin/activate
```

Then run:

```bash
python server.py
```

The server uses stdio, which is the common MCP mode for local command-line
agents.

## Available Tools

### `search_food_inspections`

Searches the NY food service establishment last-inspection dataset.

Parameters:

- `query`: optional text search, such as a facility name or violation term
- `city`: optional city filter
- `county`: optional county filter
- `min_critical_violations`: optional minimum number of critical violations
- `max_results`: maximum records to return, from 1 to 25

## Example Questions

- Use the NY food inspection MCP server to find Albany restaurants with at
  least one critical violation.
- Search for food inspection records for "Dunkin" in Monroe County.
- Find NY food service inspections mentioning "rodent" and summarize the
  results.

## Test With MCP Inspector

From this folder:

```bash
npx @modelcontextprotocol/inspector python server.py
```

Then open the Inspector web UI and try the `search_food_inspections` tool.

## Known Limitations

- The dataset only reports each establishment's most recently reported
  inspection.
- Violation text is summarized; detailed inspection report fields and corrective
  actions are not included.
- Public API availability and rate limits are controlled by the NY Health Data
  portal.
