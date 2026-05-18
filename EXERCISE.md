# Exercise: Using MCP Servers to Improve Public Information Access


## Overview

In this exercise, you'll improve access to public information by building an [MCP server](https://modelcontextprotocol.io/docs/learn/server-concepts) that exposes published state data to agentic AI applications. Along the way, you'll have a chance to try out the latest AI coding tools and get advice from engineers from top labs.


## 1. Setup

See the [README.md](README.md) for basic setup. Before starting this exercise, make sure you have access to:

- GitHub for sharing code
- Codespaces for cloud-based development, or an equivalent local environment
- AI agents, coding tools, and usage credits from your engineering mentor


## 2. Pick a public data source to work with

Choose a public information resource to wrap with an MCP server, ideally from your state or an adjacent one.

Look for a source that ideally:

- Has strong public value
- Useful search or filtering capabilities
- Exposes structured or semi-structured data
- Does not already have an MCP server implementation
- Does not require complex authentication

Good examples might include:

- State procurement data
- Legislative bill data
- Public meeting records
- State budget data
- Business registrations
- Environmental permits
- Public salary data
- Court or administrative records
- Lobbying disclosures


## 3. Try using the data source directly

Run a few test queries using the website, API, portal, or downloadable
dataset. What does it do well and what's left to be desired?


## 4. Build your MCP server

Use your preferred AI coding assistant to create an MCP server that exposes your chosen data source. 

1. Create a subdirectory under [coffee-code](https://github.com/CCF-AI-Officers-Summit-2026/coffee-code) to contain your work. Give it a descriptive name like {state}-{datasource} (e.g., coffee-code/wa-procurement)
2. Configure your AI coding tool to use this new directory as your project home.
3. Experiment with prompts for generating a MCP for your chosen resource in your preferred choice of programming language. Popular choices are python or typescript/javascript, but an MCP server can be written in any language.
5. Review the generated code. Does it seem correct and well designed? Are there any changes you'd want to make? Try asking your AI coding agent questions about the implementation. For example, is it a stdio or streamable HTTP server?
6. To interact with your new MCP server, you'll need a client. [mcp-inspector](https://github.com/modelcontextprotocol/inspector) can be a useful tool for seeing what interfaces your server exposes and inspecting responses. To invoke it, run `npx @modelcontextprotocol/inspector` You can then give the web UI the command to start your MCP server. 

Once you're satisfied, make sure you leave a README file that helps others install and reuse the server. This is also a good time to check in your code and submit a pull request to merge with the main repository. See [README.md](README.md) for a quick cheat sheet on how to do this.


## 5. Connect your MCP server to an AI agent

Configure your favorite agentic AI application to work with your MCP server. Not every agentic AI application supports MCP servers, so you may need to do a bit of research. Here are some examples of tools that should support MCP:

- [Gemini command-line](https://geminicli.com/docs/tools/mcp-server/#how-to-set-up-your-mcp-server)
- [Claude Code](https://code.claude.com/docs/en/mcp)
- [Claude Desktop](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)
- [Codex](https://developers.openai.com/codex/mcp)

Many tools require editing a configuration file to add an MCP server. Your AI coding agent may be able to help with this if you have questions or get stuck.

After configuring your MCP server, try several prompts to check whether your AI agent returns accurate results. Did it correctly interpret your queries and the data returned from your MCP server. If not how would you correct this?


## 6. Reflection

As a team, explore:

- Is the user experience better or worse through an AI agent vs. the original web interface?
- What can users now do that was hard to do before?
- What still feels risky, confusing, or incomplete?
- Can the agent explain its responses and reasoning?
- Does it preserve important context and caveats that you provided?
- Could a non-expert use this successfully?
- What mistakes might the agent make?


## 7. Demo Preparation

Prepare a short 2-3 minute demo that showcases your work. Consider:

1. The public data source you selected
2. A real user need or question
3. How your MCP server helps the agent answer that question
4. What is better, faster, or more accessible than the original interface
5. A limitation or risk you discovered
6. One improvement you would make next

Keep the demo focused. A good demo addresses one clear need well.


## 8.Follow-On Improvements

Consider improving your MCP server to improve your demo. For example:

- Streaming HTTP for remote access (e.g., so a local AI agent can talk to a server running on your codespace)
- Schema documentation so agents understand the data better
- Caching results to make responses faster
- Better filtering by date, agency, vendor, amount, geography, or category
- Aggregations such as totals, counts, rankings, or trends
- Query rewriting to translate plain-language questions into structured filters
- Support for comparing records across agencies or time periods
- Logging to understand which queries users ask most often
- Guardrails for sensitive or easily misinterpreted data

You may also want to explore how multiple MCP servers can 

## 9. Demo

**Demo length:** 3 minute demo, 1 minute Q&A

We only have 30 minutes for all team demos, so please be prepared and keep to time. 

*Tip: short demo times might require showing chat transcripts in place of long interactions, or caching MCP server results.*


