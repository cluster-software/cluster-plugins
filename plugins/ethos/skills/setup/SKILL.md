---
name: setup
description: Set up or repair Ethos in Codex by installing and authenticating ethos-cli, verifying the marketplace plugin and hosted MCP server, and confirming the active organization. In Claude Desktop/Cowork, direct the user to the manual plugin installation flow instead of running setup commands.
allowed-tools: Bash, Read, mcp__ethos__get_current_ethos_org
catalog_visible: false
---

# Ethos setup

## Route by product

- **Codex:** complete the automated workflow below.
- **Claude Desktop/Cowork:** do not run shell commands or attempt to install the
  plugin, CLI, or MCP server. Present the Claude steps and Loom video in
  `GETTING_STARTED.md`, then stop.

If the current product is ambiguous, do not run setup commands until it is
clear that this is Codex.

Verification must be read-only. Do not create or change Ethos tables, agents,
campaigns, or contacts.

## 1. Install and authenticate the CLI

Preserve a working CLI:

```bash
command -v ethos >/dev/null 2>&1 && ethos --version
```

If `ethos` is missing, require Node.js 20 or newer and npm:

```bash
command -v node >/dev/null 2>&1 && node --version
command -v npm >/dev/null 2>&1 && npm --version
```

If a prerequisite is missing, leave the plugin installed and tell the user what
to install from https://nodejs.org. Do not install or replace a machine-level
Node runtime automatically.

Use the installer command from the originating setup prompt and apply
`ETHOS_AGENT_CLIENT=codex` to its installer shell. If none was provided, use the
production installer with the Codex client selected:

```bash
curl -fsSL "https://api.ethos.hello-cluster.com/v1/auth/cli/install" | ETHOS_AGENT_CLIENT=codex bash
```

Allow at least two minutes. The installer starts the combined CLI and MCP
authorization flow. Do not expose tokens printed or stored by either client.

Check the CLI credential:

```bash
ethos auth status --json
```

If the JSON reports `authenticated: false`, run:

```bash
ethos auth login --agent-client codex --with-codex-mcp
```

Do not run a plain CLI login first. After browser approval, require
`ethos auth status --json` to report `authenticated: true`; a zero exit code is
not sufficient.

Install the prompt hook idempotently:

```bash
ethos hooks install
```

Ethos skills come from the marketplace plugin. Do not install or overwrite
separate CLI-managed copies.

## 2. Verify the plugin and MCP registration

Inspect the plugin:

```bash
codex plugin list --json
```

Require `ethos@cluster-plugins` to report `installed: true` and `enabled: true`.
If it does not, return to the Codex installation branch in
`GETTING_STARTED.md`.

Inspect the MCP server:

```bash
codex mcp get ethos --json
```

Require `enabled: true`, transport type `streamable_http`, and URL
`https://api.ethos.hello-cluster.com/mcp`. Stop and report any mismatch.

If the combined installer did not perform MCP OAuth because the CLI was already
authenticated, run:

```bash
codex mcp login ethos
```

Open the browser approval and wait for the callback. Do not assume that calling
an unavailable MCP tool will initiate OAuth, and do not run a second MCP login
when the combined flow already completed.

## 3. Verify the organization

If `get_current_ethos_org` is available in this task, call it directly with no
arguments. Otherwise run a fresh ephemeral verification process without making
the user switch tasks:

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

For the ephemeral path, require a completed `mcp_tool_call` for server `ethos`
and tool `get_current_ethos_org`, with no error and a result whose status is
`ok`.

Setup succeeds only when CLI authentication passes, the plugin and MCP server
are enabled, and the read-only tool returns the active organization.

## 4. Give the user next steps

Report the organization name and ID, tell the user Ethos is ready, and suggest:

- `$ethos:find-people` — find prospects from a natural-language ICP.
- `$ethos:find-people-at-companies` — upload a company CSV and find the right
  people at those companies.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Marketplace or plugin command is blocked by managed policy | Report the policy restriction and ask the user's administrator to allow `cluster-software/cluster-plugins`; do not bypass it. |
| The installed plugin is missing `ethos:setup` | Update the marketplace/plugin, locate the cached `skills/setup/SKILL.md` using `GETTING_STARTED.md`, and follow it directly. |
| Node.js or npm is missing | Leave the plugin installed and guide the user to install Node.js 20+ before resuming. |
| Combined approval reports a temporary server failure | Retry on the same approval page; do not create another CLI claim or authorization URL. |
| Combined approval succeeds but localhost return is blocked | Use **Return to Codex** on the same approval page. |
| CLI is authenticated but MCP asks for auth | Run `codex mcp login ethos` before ephemeral verification. |
| MCP tools are absent | Verify `codex plugin list --json` and `codex mcp get ethos --json`, complete OAuth if needed, then run scoped ephemeral verification. |
