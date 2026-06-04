# NY Food Service Inspection MCP Server

This project builds a small MCP server for the New York State Department of
Health dataset, **Food Service Establishment: Last Inspection**.

Project creator: Albert Pulido, New York State Deputy Secretary for Finance & Technology
Tech Support by [Mark Headd](https://github.com/mheadd) 

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

## Use With Claude Desktop

Claude Desktop can run local MCP servers over stdio. This works well for this
project because `server.py` already starts a stdio MCP server.

First, make sure the server is installed locally:

```bash
cd /Users/markheadd/Repos/coffee-code/ny-food-inspections
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m py_compile server.py
```

Then open Claude Desktop and edit the config file:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

On macOS, this config connects Claude Desktop to the server:

```json
{
  "mcpServers": {
    "ny-food-inspections": {
      "command": "/Users/markheadd/Repos/coffee-code/ny-food-inspections/.venv/bin/python",
      "args": [
        "/Users/markheadd/Repos/coffee-code/ny-food-inspections/server.py"
      ]
    }
  }
}
```

If your project is in a different folder, replace both paths with your actual
absolute paths. After saving the file, fully quit and reopen Claude Desktop.

Try this prompt:

```text
Use the ny-food-inspections MCP server to find Albany food service
establishments with at least 1 critical violation. Show the source dataset.
```

If the server does not appear in Claude Desktop, check the MCP logs:

```bash
tail -n 20 -f ~/Library/Logs/Claude/mcp*.log
```

Claude Desktop setup reference:
https://modelcontextprotocol.io/docs/develop/connect-local-servers

## ChatGPT Testing Note

This same local stdio approach is not supported directly by ChatGPT. Claude
Desktop can start a local command from `claude_desktop_config.json`, but ChatGPT
connects to MCP apps as remote connectors in ChatGPT web.

Good options for testing with ChatGPT are:

- Use OpenAI Secure MCP Tunnel to connect this local stdio server without
  exposing it publicly.
- Convert or deploy the server as a remote MCP server with a supported HTTP
  transport, then add it as a custom ChatGPT app or connector.
- Keep using MCP Inspector, Claude Desktop, or Codex for local stdio testing.

ChatGPT MCP app reference:
https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt

OpenAI Secure MCP Tunnel reference:
https://developers.openai.com/api/docs/guides/secure-mcp-tunnels

## Known Limitations

- The dataset only reports each establishment's most recently reported
  inspection.
- Violation text is summarized; detailed inspection report fields and corrective
  actions are not included.
- Public API availability and rate limits are controlled by the NY Health Data
  portal.
