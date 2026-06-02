# Coffee & Code: Codex CLI + MCP In GitHub Codespaces

This guide helps workshop participants create a GitHub Codespace, install the
Codex CLI, sign in with device authentication, and use Codex to build an MCP
server for public government data.

The full workshop exercise lives in `EXERCISE.md`. Treat that file as the
source of truth for the required build steps.

## Workshop Context

This is the CCF AI Officers Summit 2026 **Coffee & Code** event. Participants
are government AI officers building MCP servers that wrap public state data so
AI agents can access it.

Participants may be new to Git, Codespaces, terminal commands, Python, and
software development. Codex is most useful when you ask it to explain what it is
doing, make one change at a time, and verify each step before moving on.

This workshop spans two days. Codespaces can time out or be deleted. Git is the
only reliable way to save progress, so commit and push before lunch, before the
end of each day, and before any long break.

## 1. Create A New Codespace

1. Open the workshop repository in GitHub.
2. Select **Code**.
3. Select the **Codespaces** tab.
4. Select **Create codespace**.
5. Wait for the Codespace to finish loading.

After the Codespace opens, use the built-in terminal for the rest of this guide.

## 2. Install The Codex CLI

In the Codespace terminal, install the Codex CLI using one of the following
methods.

### macOS/Linux

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

### Windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

### npm

```bash
npm install -g @openai/codex
```

### Homebrew

```bash
brew install --cask codex
```

Confirm Codex is installed:

```bash
codex --version
```

## 3. Sign In With Device Authentication

In Codespaces, use device authentication. It avoids the `localhost` browser
callback issue that can happen when a CLI is running in a remote environment.

```bash
codex login --device-auth
```

Codex will show a link and a one-time device code in the terminal.

1. Open the link in your browser.
2. Sign in to the **Coffee & Code 6/4 ChatGPT Workspace** using the email and
   password associated with your account.
3. Enter the device code shown in the Codespace terminal.
4. Return to the Codespace terminal when the login completes.

If Codex falls back to a regular browser login and then shows a `localhost`
connection error, ask a facilitator to confirm device code login is enabled for
the workspace.

## 4. Start Codex In The Repository

From the workshop repository directory in the Codespace terminal, run:

```bash
codex
```

Codex starts in the current directory. It can read repository files, edit code,
run terminal commands, explain errors, and help you test your MCP server.

## 5. Start With This Codex Prompt

Paste this into Codex after it opens:

```text
Read EXERCISE.md and guide me through this workshop step by step.

I am building an MCP server for public government data in GitHub Codespaces.
I may be new to Git, terminal commands, Python, and software development.

Be patient and concrete. Before making changes, explain the next step. When
something breaks, explain what happened before fixing it. Help me test each
step, and remind me to commit and push before I stop for the day.
```

Useful follow-up prompts:

```text
Show me the current project structure and explain which files matter for this
exercise.
```

```text
Help me pick one public state data source that will work well for an MCP server.
Favor sources with public APIs or downloadable CSV/JSON data.
```

```text
Make the smallest working MCP server first. Start with one useful tool, test it,
then help me add more.
```

```text
Before changing code, tell me what file you plan to edit and why.
```

```text
Show me the diff and explain what changed in plain English.
```

## 6. What MCP Means In This Workshop

MCP stands for **Model Context Protocol**. It is a standard way for an AI agent
to use external tools and data sources.

In this workshop, the system looks like this:

```text
Participant question
        |
        v
Codex CLI
        |
        | MCP tool call
        v
Your MCP server
        |
        | HTTP request, API query, CSV lookup, or data-file search
        v
Public government data source
```

Your MCP server is the bridge between the AI agent and the public data source.
It should expose a small set of clear tools, such as:

- `search_contracts`
- `get_contract_details`
- `list_agencies`
- `search_bills`
- `get_budget_line_items`

Good MCP tools have:

- Clear names that describe the action.
- Clear descriptions that tell Codex when to use the tool.
- Parameters that match how users naturally ask questions.
- Helpful error messages when data is missing, ambiguous, or unavailable.
- Source URLs or notes that make the public data source traceable.

## 7. Day 1 Build Flow

Use this flow with Codex while working through `EXERCISE.md`.

### Pick A Public Data Source

Ask Codex:

```text
Help me choose a public state data source for this MCP server. Ask me what state
or policy area I care about, then suggest data sources that have public APIs or
downloadable structured data.
```

Good workshop data sources usually have:

- Public access without private credentials.
- A public API, CSV, JSON, Socrata endpoint, CKAN endpoint, or downloadable
  dataset.
- A clear civic use case, such as procurement, legislation, budgets, permits,
  licenses, environmental monitoring, campaign finance, or public meetings.

### Explore The Data Before Coding

Ask Codex:

```text
Before we write code, help me inspect this data source. Identify the API or
download format, the useful fields, example queries, limitations, and one plain
English question this MCP server should answer first.
```

Do not start with a broad scraper. Prefer official APIs and structured downloads
when available.

### Build One Tool First

Ask Codex:

```text
Use the starter template from EXERCISE.md. Build only one MCP tool first: the
most useful search or lookup tool for my selected public data source. Keep the
change small and explain every file you edit.
```

Start with one tool, test it, and then add more. A working small server is
better than an unfinished large one.

### Review The Server

Ask Codex:

```text
Review the MCP server we built. List every tool by name, explain what it does,
show example questions a real user could ask, and identify one gap we may want
to fix next.
```

### Write A Project README

Ask Codex:

```text
Create or update the README for my MCP server. Include the public data source,
why it is useful, installation steps, how to run the server, available tools,
example questions, and known limitations.
```

## 8. Connect Your MCP Server To Codex CLI

After your server runs locally, connect it to Codex CLI so Codex can use its
tools.

First, inspect the MCP commands available in your installed Codex CLI:

```bash
codex mcp --help
```

List any MCP servers already configured:

```bash
codex mcp list
```

### Option A: Add The Server With `codex mcp add`

For a local MCP server that starts from a terminal command, use `codex mcp add`.
Replace `<server-name>` and `<command that starts your server>` with the names
from your exercise:

```bash
codex mcp add <server-name> -- <command that starts your server>
```

Examples:

```bash
codex mcp add state-data -- python server.py
```

```bash
codex mcp add state-data -- npm run start
```

After adding the server, restart Codex:

```bash
codex
```

Then ask:

```text
Tell me which MCP servers and tools you can see. Use the workshop MCP server and
test each tool with one simple query.
```

### Option B: Add The Server In `~/.codex/config.toml`

If the CLI add command is confusing, or if you need to set the working
directory explicitly, add the server to your Codex config.

Open `~/.codex/config.toml` and add a block like this:

```toml
[mcp_servers.state-data]
command = "python"
args = ["server.py"]
cwd = "/workspaces/coffee-code/STATE-DATASOURCE"
startup_timeout_sec = 20
tool_timeout_sec = 60
```

Replace:

- `state-data` with a short server name.
- `/workspaces/coffee-code/STATE-DATASOURCE` with the actual folder that
  contains your server.
- `python` and `server.py` with the command from `EXERCISE.md` if your server
  starts differently.

Restart Codex after changing `~/.codex/config.toml`.

## 9. Test The MCP Connection

Once the server is configured, ask Codex:

```text
Use my configured MCP server. First tell me the tools you can see. Then run the
simplest possible test query for each tool and explain the result.
```

Then try the real question that motivated the project:

```text
Use my MCP server to answer this question: <your plain-English question>. Cite
which public data source the answer came from and call out any limitations.
```

If Codex does not use the MCP tool, be explicit:

```text
Use the <tool_name> MCP tool from my <server-name> server to answer this.
```

## 10. Save Your Work Before You Stop

Before lunch, before the end of Day 1, and before any long break:

```bash
git status
git checkout -b YOUR-BRANCH-NAME
git add .
git commit -m "Save Coffee and Code MCP progress"
git push -u origin YOUR-BRANCH-NAME
```

If you already created a branch, use:

```bash
git status
git add .
git commit -m "Save Coffee and Code MCP progress"
git push
```

Ask Codex to help if Git returns an error:

```text
Explain this Git error in plain English and tell me the safest next command.
Do not discard my work.
```

## 11. Day 2 Resume Flow

When you return on Day 2:

```bash
git status
git branch
git pull
```

If your Codespace was deleted and you created a new one, restore your branch:

```bash
git fetch origin
git checkout YOUR-BRANCH-NAME
```

Then reinstall dependencies inside your project folder if needed:

```bash
pip install -r requirements.txt
```

Ask Codex:

```text
Read EXERCISE.md and my current project files. Summarize what I built yesterday,
verify the MCP server still runs, and help me continue from the next unfinished
step.
```

## 12. Improve The Server

After the first MCP tool works, choose one or two improvements that strengthen
the demo:

- Better tool descriptions so Codex chooses the right tool.
- Additional filters such as agency, date, amount, geography, category, or
  status.
- Aggregations such as totals, counts, rankings, or trends.
- Clearer error messages for empty results or bad input.
- Caching sample results if the live API is slow.
- README examples that show realistic user questions.

Ask Codex:

```text
Suggest two improvements that would make this MCP server more useful for a
3-minute public-sector demo. Pick the safest one to implement first.
```

## 13. Prepare A 3-Minute Demo

Ask Codex:

```text
Help me prepare a 3-minute demo of this MCP server. Include the problem, the
public data source, the MCP tools I built, one live question to ask, one
limitation, and one next improvement.
```

Recommended structure:

1. **Problem**: what public data is hard to use today.
2. **Data source**: what official source the server wraps.
3. **MCP tools**: what the server exposes.
4. **Live demo**: ask one plain-English question and show Codex using the tool.
5. **Reflection**: what is better, what is still risky, and what you would add
   next.

Before the demo, capture a working example question and answer in your README
or notes. Live APIs can be slow or unavailable.

## 14. Common Codex CLI And MCP Problems

### `localhost refused to connect` during login

Use device authentication:

```bash
codex login --device-auth
```

This is common in Codespaces because the CLI is running remotely but the browser
is running locally.

### Codex cannot find my MCP server

Check:

```bash
codex mcp list
```

Then inspect `~/.codex/config.toml`. Confirm:

- The server name is correct.
- `command` and `args` start the server.
- `cwd` points to the folder containing your server.
- You restarted Codex after changing config.

### The MCP server crashes on startup

Run the server command directly in the terminal:

```bash
python server.py
```

If there is an error, paste it into Codex and ask:

```text
Explain this server startup error before fixing it. Make the smallest safe
change, then show me how to test it again.
```

### `ModuleNotFoundError`

Install dependencies from the MCP server project folder:

```bash
pip install -r requirements.txt
```

### Public API is down or blocked from Codespaces

Ask Codex to confirm the failure with a small request. If the public source is
temporarily unavailable, use a small sample CSV or JSON file so you can keep
building and testing the MCP interface.

### Codex is not using my tool

Improve the tool name and description. Then ask explicitly:

```text
Use the <tool_name> MCP tool. If you choose not to use it, explain why.
```

### I made changes on the wrong branch

Create a branch now. Your uncommitted changes will come with you:

```bash
git checkout -b YOUR-BRANCH-NAME
```

### `git push` is rejected

Set the upstream branch:

```bash
git push -u origin YOUR-BRANCH-NAME
```

### I do not know what state Git is in

Run:

```bash
git status
git branch
```

Paste the output into Codex and ask it to explain the safest next step.

## 15. Useful Codex CLI Commands

```bash
codex
```

Start Codex in the current repository.

```bash
codex login --device-auth
```

Sign in from Codespaces using device authentication.

```bash
codex mcp --help
```

Show MCP-related commands available in your installed Codex CLI.

```bash
codex mcp list
```

List configured MCP servers.

```bash
codex doctor
```

Generate a diagnostic report for local Codex installation, config, auth,
runtime, Git, terminal, app-server, and thread inventory issues.

## Documentation

- Codex CLI documentation: https://developers.openai.com/codex/cli
- Codex authentication: https://developers.openai.com/codex/auth
- Codex config reference: https://developers.openai.com/codex/config-reference
- Model Context Protocol: https://modelcontextprotocol.io
