---
name: setup
description: Set up or repair Ethos by verifying the marketplace plugin, installing and authenticating ethos-cli, synchronizing skills and hooks, and confirming the hosted MCP connection.
allowed-tools: Bash, Read, mcp__ethos__get_current_ethos_org
catalog_visible: false
---

# Ethos setup

Complete both Ethos surfaces:

1. `ethos-cli`, which has its own saved CLI credential.
2. The plugin's hosted MCP server.

In Codex, fresh setup obtains separate least-privilege credentials for both
surfaces through one user-facing browser approval.

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
included in the originating setup prompt. In Codex, apply
`ETHOS_AGENT_CLIENT=codex` to the installer shell so the installer uses the
combined CLI and MCP authorization flow. For the standard installer command,
run:

```bash
curl -fsSL "https://api.ethos.hello-cluster.com/v1/auth/cli/install" | ETHOS_AGENT_CLIENT=codex bash
```

Outside Codex, or if no installer command was supplied, use the production
fallback without that environment variable. The Codex installer starts
`codex mcp login ethos` and opens one combined browser approval. Allow at least
two minutes for the command. Do not expose tokens printed or stored by either
client.

## 2. Authenticate and verify the CLI

Run the status check and read its JSON result:

```bash
ethos auth status --json
```

If it reports that the CLI is not authenticated in Codex, run:

```bash
ethos auth login --agent-client codex --with-codex-mcp
```

This command starts the MCP OAuth login and uses one approval page to provision
separate CLI and MCP credentials. Do not run a plain CLI browser login first.
For other agents, use `ethos auth login --agent-client auto`. After approval,
run `ethos auth status --json` again. A zero exit code alone is insufficient if
the JSON says `authenticated: false`.

If the approval page reports a temporary server failure, use its retry action
on the same page. The combined authorization is resumable: do not start a
second CLI claim or reopen the authorization URL.

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

## 3. Prepare the plugin MCP server

If the `get_current_ethos_org` MCP tool is already available in this task, skip
to the read-only verification below. Otherwise, use the matching agent flow.

### Codex

Keep the user in the current task throughout setup.

First inspect the plugin state:

```bash
codex plugin list --json
```

Require the `ethos@cluster-plugins` entry to report `installed: true` and
`enabled: true`. If it does not, return to the installation steps in
`GETTING_STARTED.md`; do not continue to OAuth.

Next inspect the registered MCP server:

```bash
codex mcp get ethos --json
```

Require `enabled: true`, transport type `streamable_http`, and URL
`https://api.ethos.hello-cluster.com/mcp`. If the server is missing, disabled,
or points elsewhere, report the observed state and stop. Do not treat every
missing tool as only a stale-task problem.

If the combined command above did not run because the CLI was already
authenticated, initiate MCP OAuth explicitly:

```bash
codex mcp login ethos
```

Open the browser approval and wait for the callback. Require the command to
finish successfully. If the combined CLI command already completed, do not run
a second MCP login. Do not assume that calling an unavailable MCP tool will
start OAuth.

After all three checks pass, launch a fresh ephemeral Codex process from this
task to load the newly installed MCP tool and perform only the read-only
verification:

```bash
codex exec \
  --ephemeral \
  --json \
  --sandbox read-only \
  --skip-git-repo-check \
  -c 'mcp_servers.ethos.url="https://api.ethos.hello-cluster.com/mcp"' \
  -c 'mcp_servers.ethos.tools.get_current_ethos_org.approval_mode="approve"' \
  'Use only the Ethos MCP server. Call the read-only get_current_ethos_org tool with no arguments. Do not run shell commands, edit files, or call any write tool. Return whether the call succeeded and the organization name and ID.'
```

The approval override applies only to `get_current_ethos_org`; do not broaden it
to the server or any write tool. Inspect the JSON event stream and require a
completed `mcp_tool_call` for server `ethos`, tool `get_current_ethos_org`, with
no error and a result whose status is `ok`. Report the returned organization in
the original task. Do not ask the user to create, reopen, or switch tasks.

### Claude Code

If the MCP tool is unavailable after plugin installation, ask the user to run
`/reload-plugins`, then invoke `/ethos:setup` again in this conversation.

Do not repeatedly reinstall the plugin to solve a stale task.

## 4. Authenticate and verify MCP

Call the read-only `get_current_ethos_org` tool with no arguments. In Codex, use
the direct tool when it was already available in the original task; otherwise
use the successful ephemeral verification result above. In Claude Code, the
agent host may open a separate OAuth approval because MCP does not reuse the CLI
token.

Setup is complete only when the tool returns the active Ethos organization.
Report the organization name and ID along with the successful CLI status. Do not
use a write tool as a connection test.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Marketplace or plugin command is blocked by managed policy | Report the policy restriction and ask the user's administrator to allow `cluster-software/cluster-plugins`; do not bypass it. |
| The plugin installed but `ethos:setup` is missing | Update the marketplace/plugin, locate `skills/setup/SKILL.md` with the command in `GETTING_STARTED.md`, and follow it directly. |
| Node.js or npm is missing | Leave the plugin installed, guide the user to install Node.js 20+ from nodejs.org, then resume this skill. |
| Combined Codex approval reports a temporary server failure | Retry on the same approval page. Do not start a second CLI claim or recreate the authorization URL. |
| Combined Codex approval succeeds but the automatic localhost return is blocked | Use the **Return to Codex** button on the same approval page. Do not reopen or recreate the authorization URL. |
| CLI is already authenticated but MCP asks for auth | In Codex run `codex mcp login ethos` before the ephemeral verification. |
| MCP tools are absent in Claude Code | Run `/reload-plugins`; if they remain absent, fully restart Claude Code and retry the skill. |
| MCP tools are absent in Codex | Inspect `codex plugin list --json` and `codex mcp get ethos --json`; if the combined auth command did not already complete, run `codex mcp login ethos`, then run the scoped ephemeral verification without switching tasks. |
