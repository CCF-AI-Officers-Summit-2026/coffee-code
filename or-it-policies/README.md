# Oregon IT Policy Search — MCP Server

An MCP server that lets AI assistants search across Oregon's statewide IT policies. Instead of opening individual PDFs on the DAS website, just ask a question in plain English.

## Data Source

[Oregon DAS Statewide Policies](https://www.oregon.gov/das/Pages/policies.aspx#IT) — 22 IT policies covering cybersecurity, cloud systems, data governance, incident response, acceptable use, and more.

Policies are stored as local PDF copies extracted at startup. Two older policies (107-004-051, 107-004-053) are scanned images and not searchable.

## Setup

```bash
cd or-it-policies
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
| `list_policies` | List all 22 policies with numbers and titles |
| `search_policies(query)` | Search full text of all policies by keyword or phrase |
| `get_policy(policy_number)` | Get the full text of a specific policy |

## Example Queries

- "What does Oregon policy say about cloud security?"
- "Find policies that mention incident response"
- "What are the rules for acceptable use of state IT assets?"
- "Show me the data governance policy"
- "What policies cover remote work?"
