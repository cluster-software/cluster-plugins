---
name: setup
description: Set up or repair Ethos by verifying the marketplace plugin and hosted MCP connection, plus the required CLI on local Claude Code and Codex or the optional CLI in Claude Desktop/Cowork.
allowed-tools: Bash, Read, mcp__ethos__get_current_ethos_org
catalog_visible: false
---

# Ethos setup

First identify the current host as one of:

- local Claude Code,
- Claude Desktop/Cowork, or
- Codex.

Use the product that is running this skill as the source of truth. Do not infer
Claude Desktop/Cowork from a failed network request alone, and do not infer
local Claude Code from the presence of a `claude` command: the Desktop/Cowork
sandbox VM ships its own `claude` CLI whose configuration is sandbox-local,
never read by the app, and discarded after the session. If the host is
ambiguous, apply the stricter local Claude Code CLI requirements, but never
trust shell `claude plugin` output until the host is confirmed to be local
Claude Code.

Local Claude Code includes local sessions run by the Claude desktop app: they
use the real `~/.claude` configuration, but interactive commands such as
`/plugin`, `/reload-plugins`, and `/mcp` can be unavailable there. Treat such a
host as local Claude Code, and when a required interactive command is
unavailable, use the new-conversation remediation described in step 3 instead
of insisting on the command.

In every Claude host, plugin installation goes through the user — slash
commands in Claude Code, the app plugin UI in Claude Desktop/Cowork. Never
install the plugin by running `claude plugin ...` through the shell.

The completion requirements depend on that host:

- Local Claude Code and Codex require a working, authenticated `ethos-cli`, the
  installed plugin, and the plugin's authenticated hosted MCP server.
- Claude Desktop/Cowork requires the installed plugin and authenticated hosted
  MCP server. Its CLI is best-effort because sandbox egress can be denied by an
  organization allowlist.

In Codex, fresh setup obtains separate least-privilege credentials for both
surfaces through one user-facing browser approval.

Never treat the CLI as a substitute for MCP verification. Verification must be
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
major version is below 20, tell the user exactly what is missing. In local
Claude Code or Codex, stop the CLI portion and ask the user to install a current
Node.js LTS release from https://nodejs.org, then resume this skill. In Claude
Desktop/Cowork, record the optional CLI as unavailable and continue to plugin
and MCP verification. Never install or replace a machine-level Node runtime
automatically.

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

If the installer or another CLI authentication request fails in Claude
Desktop/Cowork, inspect the failed proxy response. If necessary, repeat only a
read-only request, print its response headers, and discard its body:

```bash
curl --silent --show-error --dump-header - --output /dev/null \
  "https://api.ethos.hello-cluster.com/v1/auth/cli/install" 2>&1
```

Only the case-insensitive response header
`X-Proxy-Error: blocked-by-allowlist` authorizes the sandbox exception. When it
is present:

1. Record `CLI skipped: Claude sandbox allowlist blocks the Ethos CLI endpoint`.
2. Do not retry, alter proxy settings, copy credentials, or attempt another
   download route.
3. Skip CLI authentication and continue to plugin and MCP verification.

Do not classify a generic HTTP 403, DNS failure, timeout, TLS error, or missing
`curl` as an allowlist block. Report other CLI failures accurately. They remain
non-blocking only in Claude Desktop/Cowork; in local Claude Code and Codex they
must be resolved before setup can succeed.

## 2. Authenticate and verify the CLI

Skip this section when the Claude Desktop/Cowork CLI was recorded as optional
and unavailable.

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

Install the prompt hook explicitly. This command is idempotent and repairs a
postinstall that was skipped or interrupted:

```bash
ethos hooks install
```

Ethos skills come from the installed marketplace plugin; do not install or
overwrite separate CLI-managed copies.

## 3. Verify the plugin and prepare its MCP server

Always verify the marketplace plugin before MCP, even if a server with an Ethos
tool is already available. Tool availability alone does not prove that
`ethos@cluster-plugins` is installed and enabled. Use the matching agent flow.

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

### Local Claude Code

Installation is the user's job — the two `/plugin` slash commands in
`GETTING_STARTED.md`. The shell command below is read-only inspection, never a
substitute for them.

Inspect the plugin state:

```bash
claude plugin list --json
```

Require `ethos@cluster-plugins` to be installed and enabled. If it is missing,
show the user the exact slash commands from `GETTING_STARTED.md`
(`/plugin marketplace add cluster-software/cluster-plugins`, then
`/plugin install ethos@cluster-plugins`), wait for them to confirm they ran
both, and inspect again.

After the plugin check, if the MCP tool is already available, continue directly
to the read-only call in step 4. If it is unavailable, inspect the registered
MCP server before prescribing any remediation:

```bash
claude mcp list
```

A healthy install lists
`plugin:ethos:ethos: https://api.ethos.hello-cluster.com/mcp (HTTP)`, typically
marked `Needs authentication` before OAuth. Interpret the output:

- The `plugin:ethos:ethos` entry is listed: the session is stale. Ask the user
  to run `/reload-plugins`, then invoke `/ethos:setup` again in this
  conversation. If `/reload-plugins` is unavailable in this host (Claude
  desktop app local sessions), MCP servers load only at session start: ask the
  user to start a new conversation and invoke `/ethos:setup` there.
- The entry is missing even though the plugin is installed and enabled: the
  plugin's `.mcp.json` did not register. Claude Code silently skips MCP server
  entries it cannot parse (for example, a `url` entry without
  `"type": "http"`), so an absent entry with no warning still means a config
  problem, not a stale session. Have the user run
  `/plugin marketplace update cluster-plugins` then
  `/plugin update ethos@cluster-plugins` to pick up a fixed plugin version and
  re-check. If the entry is still missing after the update, report the plugin
  version and this exact symptom as a plugin configuration bug and stop.

Do not repeatedly ask the user to reinstall the plugin to solve a stale
session, and do not loop on reload for a missing-entry state that reload cannot
fix.

### Claude Desktop/Cowork

Never run `claude plugin` commands here, not even for inspection: the shell
executes inside a sandbox VM with its own `claude` CLI, so its output describes
the sandbox, not the app, and can report `installed: true` while the app has no
plugin.

The plugin is verified by the running app itself: require the fully qualified
`ethos:setup` skill to be registered by the host. Merely finding a cached
`SKILL.md` on a filesystem does not prove that the plugin is enabled.

If the skill is not registered, walk the user through the app UI install from
`GETTING_STARTED.md`: open **Customize → Plugins**, **Add marketplace** with
`cluster-software/cluster-plugins`, then **Browse plugins → Ethos → Install**.
Then have the user fully quit and reopen Claude — the Desktop app has no
`/reload-plugins` — and invoke `/ethos:setup` in a new conversation.

A skipped optional CLI does not relax the plugin requirement.

## 4. Authenticate and verify MCP

Call the read-only `get_current_ethos_org` tool with no arguments. In Codex, use
the direct tool when it was already available in the original task; otherwise
use the successful ephemeral verification result above. In Claude, the agent
host may open a separate OAuth approval because MCP does not reuse the CLI token.

Setup is complete only when the tool returns the active Ethos organization.
For local Claude Code and Codex, report the organization name and ID along with
the successful CLI status. For Claude Desktop/Cowork, report the organization
and one of `CLI ready` or the specific optional CLI skip reason. Do not use a
write tool as a connection test.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Marketplace or plugin command is blocked by managed policy | Report the policy restriction and ask the user's administrator to allow `cluster-software/cluster-plugins`; do not bypass it. |
| The plugin installed but `ethos:setup` is missing | In local Claude Code or Codex, update the marketplace/plugin, locate `skills/setup/SKILL.md` with the command in `GETTING_STARTED.md`, and follow it directly. In Claude Desktop/Cowork, fully quit and reopen the app; if the skill is still missing, redo the app-UI install. |
| `claude plugin list` in Claude Desktop/Cowork reports Ethos installed but the app shows no plugin or skills | That output comes from the sandbox VM's own `claude`, not the app. Ignore it, install through **Customize → Plugins**, and fully restart Claude. |
| Node.js or npm is missing | In local Claude Code or Codex, leave the plugin installed and guide the user to install Node.js 20+ before resuming. In Claude Desktop/Cowork, report the optional CLI as unavailable and continue to MCP. |
| Claude Desktop/Cowork CLI request returns `X-Proxy-Error: blocked-by-allowlist` | Skip the optional CLI, do not bypass the proxy, and continue to required plugin and MCP verification. An administrator may allowlist `api.ethos.hello-cluster.com` for future conversations if CLI access is desired. |
| Combined Codex approval reports a temporary server failure | Retry on the same approval page. Do not start a second CLI claim or recreate the authorization URL. |
| Combined Codex approval succeeds but the automatic localhost return is blocked | Use the **Return to Codex** button on the same approval page. Do not reopen or recreate the authorization URL. |
| CLI is already authenticated but MCP asks for auth | In Codex run `codex mcp login ethos` before the ephemeral verification. |
| MCP tools are absent in Claude | In Claude Code run `claude mcp list` first: if `plugin:ethos:ethos` is listed, run `/reload-plugins` (or start a new conversation where that command is unavailable); if it is missing, update the marketplace and plugin — reload cannot fix an entry Claude skipped at parse time. In Claude Desktop/Cowork fully quit and reopen the app. Then retry the skill. |
| MCP tools are absent in Codex | Inspect `codex plugin list --json` and `codex mcp get ethos --json`; if the combined auth command did not already complete, run `codex mcp login ethos`, then run the scoped ephemeral verification without switching tasks. |
