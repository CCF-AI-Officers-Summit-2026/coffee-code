# Exercise: Using MCP Servers to Improve Public Information Access


## Overview

In this exercise, you'll improve access to public information by building an [MCP server](https://modelcontextprotocol.io/docs/learn/server-concepts) that exposes state data to agentic AI applications. Along the way, you'll have a chance to try out the latest AI coding tools and get advice from engineers from top labs.


## 1. Setup

See the [README.md](README.md) for basic setup. Before starting this exercise, make sure you have access to:

- GitHub for sharing code
- Codespaces for cloud-based development, or an equivalent local environment on your laptop if you prefer
- AI agents, coding tools, and usage credits from your engineering mentor


## 2. Pick a public data source to work with

Choose a public information resource to wrap with an MCP server, ideally from your state or an adjacent one.

Look for a source that ideally:

- Has strong public value and interest
- Useful search or filtering capabilities
- Exposes structured or semi-structured data
- Does not already have an MCP server implementation
- Does not require complex authentication

Good examples might include:

- State procurement data
- Campaign finance records
- Lobbying disclosures
- Legislative bill data
- Public meeting records
- State budget data
- Business registrations
- Environmental permits
- Public salary data
- Court or administrative records


## 3. Try using the data source directly

Run a few test queries using the website, API, portal, or downloadable
dataset. Get a quick feel for what it does well and what's left to be desired.


## 4. Build your MCP server

Use your preferred AI coding assistant to create an MCP server that exposes your chosen data source. 

1. Create a subdirectory under [coffee-code](https://github.com/CCF-AI-Officers-Summit-2026/coffee-code) to contain your work. Give it a descriptive name like {state}-{datasource} (e.g., coffee-code/wa-procurement)
2. Configure your AI coding tool to use this new directory as your project home.
3. Experiment with prompts for generating a MCP for your chosen resource in your choice of programming language. Common choices are python or typescript/javascript.
4. Review the generated code. Does it seem reasonable and make sense to you?
5. To interact with your new MCP server, you'll need a client. [mcp-inspector](https://github.com/modelcontextprotocol/inspector) can be a useful tool for seeing what interfaces your server exposes and inspecting responses. To invoke it, run `npx @modelcontextprotocol/inspector` You can then give it web UI the command to run your MCP server code.


## 5. Add your MCP server 

Configure your favorite agentic AI application to work with your MCP server, e.g., 

- [Gemini command-line](https://geminicli.com/docs/tools/mcp-server/#how-to-set-up-your-mcp-server)
- [Claude Code](https://code.claude.com/docs/en/mcp)
- [Claude Desktop](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)
- [Codex](https://developers.openai.com/codex/mcp)

Try several prompts to check whether the MCP server returns accurate results with good understanding of queries and response metadata.


## 6. Reflection Questions

As a team, explore:

- Is the user experience better or worse through an AI agent?
- What can users now do that was hard to do before?
- What still feels risky, confusing, or incomplete?
- Does the agent explain where information came from?
- Does it preserve important context and caveats?
- Could a non-expert use this successfully?
- What mistakes might the agent make?


## 7. Demo Preparation

Your demo should show:

1. The public data source you selected
2. A real user need or question
3. How your MCP server helps the agent answer that question
4. What is better, faster, or more accessible than the original interface
5. One limitation or risk you discovered
6. One improvement you would make next

Keep the demo focused. A good demo answers one clear question well.

A simple README so others can install and reuse the server

## 8.Follow-On Improvements

After you have a working MCP server, consider improving it with:

- Caching results to make responses faster
- Better filtering by date, agency, vendor, amount, geography, or category
- Aggregations such as totals, counts, rankings, or trends
- Pagination support for large result sets
- Source citations and direct links to original records
- Clear error handling when the public site or API fails
- Query rewriting to translate plain-language questions into structured filters
- Schema documentation so the agent understands the data better

- Support for comparing records across agencies or time periods
- Logging to understand which queries users ask most often
- Guardrails for sensitive or easily misinterpreted data

## 9. Demo

**Demo length:** 3 minute demo, 1 minute Q&A

We only have 30 minutes for team demos, so please be prepared and keep to time. 

*Tip: the short demo times might mean showing chat transcripts instead of live demos, or using cached results.*

Your demo should explain:

1. The public data source you selected
2. A real user need or interest you addressed
3. How your MCP server and agent answered that question
4. What is better than the original interface
5. One limitation, risk, or learning you discovered (about the demo or the AI-assisted development process)

