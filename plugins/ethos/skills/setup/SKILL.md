---
name: setup
description: Set up or repair Ethos by verifying the marketplace plugin, installing and authenticating ethos-cli, synchronizing skills and hooks, and confirming the hosted MCP connection.
allowed-tools: Bash, Read, mcp__ethos__get_current_ethos_org
---

# Ethos setup

Complete both Ethos surfaces:

1. `ethos-cli`, which has its own saved CLI credential.
2. The plugin's hosted MCP server, which authenticates separately through the
   agent host.

Do not declare setup complete when only one surface works. Verification must be
read-only; do not create or change Ethos tables, agents, campaigns, or contacts.

## 1. Check the CLI and Node.js

Check whether a working CLI already exists:

```bash
command -v ethos >/dev/null 2>&1 && ethos --version
```

If that succeeds, preserve the existing CLI and continue to authentication. Do
not reinstall a working CLI just to replace it with the same package.

If `ethos` is missing, check the installer prerequisites:

```bash
command -v node >/dev/null 2>&1 && node --version
command -v npm >/dev/null 2>&1 && npm --version
```

The CLI requires Node.js 20 or newer and npm. If either is missing, or the Node
major version is below 20, stop the CLI portion and tell the user exactly what
is missing. The plugin remains installed. Ask the user to install a current
Node.js LTS release from https://nodejs.org, then resume this skill; do not
install or replace a machine-level Node runtime automatically.

When the prerequisites are present, use the exact Ethos CLI installer command
included in the originating setup prompt. If no installer command was supplied,
use the production fallback:

```bash
curl -fsSL "https://api.ethos.hello-cluster.com/v1/auth/cli/install" | bash
```

The installer opens browser approval and waits for it. Allow at least two
minutes for the command. Do not expose tokens printed or stored by the CLI.

## 2. Authenticate and verify the CLI

Run the status check and read its JSON result:

```bash
ethos auth status --json
```

If it reports that the CLI is not authenticated, run:

```bash
ethos auth login --agent-client auto
```

Complete browser approval, then run `ethos auth status --json` again. A zero
exit code alone is insufficient if the JSON says `authenticated: false`.

Synchronize the bundled skills and prompt hook explicitly. These commands are
idempotent and repair a postinstall that was skipped or interrupted:

```bash
ethos skills install
ethos hooks install
ethos skills list
```

The skills list must contain installed Ethos skills for the current agent. If a
user-managed skill with the same name was skipped, report the path and do not
overwrite it.

## 3. Load the plugin MCP server

If the `get_current_ethos_org` MCP tool is not available in this session, the
plugin was installed after the agent process loaded its tools:

- **Claude Code:** ask the user to run `/reload-plugins`, then invoke
  `/ethos:setup` again in this conversation.
- **Codex:** ask the user to start a new task, then invoke `$ethos:setup`.

Do not repeatedly reinstall the plugin to solve a stale task. Reloading or
starting the required new task is the fix.

## 4. Authenticate and verify MCP

Call the read-only `get_current_ethos_org` tool with no arguments. The agent host
may open a separate OAuth approval because MCP does not reuse the CLI token.

Setup is complete only when the tool returns the active Ethos organization.
Report the organization name and ID along with the successful CLI status. Do not
use a write tool as a connection test.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Marketplace or plugin command is blocked by managed policy | Report the policy restriction and ask the user's administrator to allow `cluster-software/cluster-plugins`; do not bypass it. |
| The plugin installed but `ethos:setup` is missing | Update the marketplace/plugin, locate `skills/setup/SKILL.md` with the command in `GETTING_STARTED.md`, and follow it directly. |
| Node.js or npm is missing | Leave the plugin installed, guide the user to install Node.js 20+ from nodejs.org, then resume this skill. |
| CLI auth succeeds but MCP asks for auth | Complete the separate MCP OAuth flow; CLI and MCP credentials are intentionally independent. |
| MCP tools are absent in Claude Code | Run `/reload-plugins`; if they remain absent, fully restart Claude Code and retry the skill. |
| MCP tools are absent in Codex | Start a new task created after plugin installation; do not continue in the pre-install task. |
