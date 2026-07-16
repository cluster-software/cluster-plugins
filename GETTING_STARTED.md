# Getting started with Ethos

> This guide is written for your coding agent. Give it this link and ask it to
> set Ethos up for you. The agent runs what it can itself and hands you the few
> steps only you can perform: client slash commands or app-UI installs, command
> approvals, browser authentication, and reloading Claude when prompted.

Ethos supports Claude and Codex through one marketplace plugin. The plugin
bundles Ethos skills and the hosted OAuth-backed MCP server. Local Claude Code
and Codex setup also installs and authenticates `ethos-cli`. In Claude
Desktop/Cowork, the plugin and MCP connection are required; the CLI is optional
because the sandbox proxy may block its installer.

This runbook is maintained alongside the marketplace. The commands below resolve
the current Ethos plugin version from marketplace metadata.

## Install or update the plugin

Use the section for the client that is running this guide.

**Agents: never install the Claude plugin by running `claude plugin ...`
through the shell.** Claude Desktop/Cowork runs shell commands inside an
isolated VM that ships its own `claude` CLI and its own throwaway `~/.claude`.
A shell install there succeeds inside the sandbox, is never read by the app,
and is discarded when the session ends, so `claude plugin list --json` from
that shell can report `installed: true` while the app has no plugin. In Claude,
plugin installation always goes through the user: slash commands in Claude
Code, the app plugin UI in Claude Desktop/Cowork.

### Claude Code

Installation is two Claude Code slash commands. The user types these at the
Claude Code prompt; agents cannot run slash commands:

```
/plugin marketplace add cluster-software/cluster-plugins
/plugin install ethos@cluster-plugins
```

If the marketplace is already configured, update instead:

```
/plugin marketplace update cluster-plugins
/plugin update ethos@cluster-plugins
```

Agents: in local Claude Code you may inspect current state with the read-only
shell commands `claude plugin marketplace list`, `claude plugin list --json`,
and `claude mcp list`, then show the user the exact slash commands their state
needs and wait for them to confirm they ran them. Continue with the setup skill
afterwards.

Local Claude Code includes local sessions run by the Claude desktop app: they
share the real `~/.claude` configuration, but interactive commands such as
`/plugin` and `/reload-plugins` can be unavailable there. When they are, install
through the app plugin UI and use a new conversation wherever this guide says
to reload.

### Claude Desktop and Cowork

Plugins install through the Claude app UI only; nothing an agent runs inside
the conversation can install one. Walk the user through:

1. Open **Customize** in the sidebar, then select **Plugins**.
2. Select **Add marketplace** and enter `cluster-software/cluster-plugins`.
3. Open **Browse plugins**, find **Ethos**, and select **Install**.
4. Fully quit and reopen the Claude app, then start a new conversation. Claude
   Desktop has no `/reload-plugins`, so a full restart is how the plugin's
   skills register.

The hosted Ethos MCP connection is authorized at the claude.ai account level;
approve the browser OAuth when the app prompts for the Ethos connector. If
organization policy hides **Add marketplace**, report that policy blocker and
ask a workspace admin to allow the marketplace; do not work around the UI.

### Codex

Inspect the configured marketplaces and plugins first:

```bash
codex plugin marketplace list
codex plugin list --available --json
```

If `cluster-plugins` is missing, add it. Otherwise upgrade it:

```bash
codex plugin marketplace add cluster-software/cluster-plugins
codex plugin marketplace upgrade cluster-plugins
```

Install or refresh Ethos. This command is idempotent when the same version is
already installed:

```bash
codex plugin add ethos@cluster-plugins --json
```

Continue the setup skill in this task. It must verify the installed plugin,
register and authenticate the MCP server, then use a fresh ephemeral Codex
process for read-only verification without making the user switch tasks.

## Run the setup skill

Continue setup in this session before reloading when possible. Invoke the fully
qualified skill for the current agent:

- Claude: `/ethos:setup`
- Codex: `$ethos:setup`

If the newly installed skill is not registered in the current session, locate
the exact installed version from the matching plugin-list command above. Then
use the matching client cache to locate its file and follow it directly as a
runbook. Set `ETHOS_PLUGIN_VERSION` yourself from the command output; do not ask
the user for it.

Local Claude Code:

```bash
ETHOS_PLUGIN_VERSION='<installed version from claude plugin list --json>'
find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}" \
  -type f -path "*/plugins/cache/*/ethos/${ETHOS_PLUGIN_VERSION}/skills/setup/SKILL.md" \
  -print -quit 2>/dev/null
```

Codex:

```bash
ETHOS_PLUGIN_VERSION='<installed version from codex plugin add/list JSON>'
find "${CODEX_HOME:-$HOME/.codex}" \
  -type f -path "*/plugins/cache/*/ethos/${ETHOS_PLUGIN_VERSION}/skills/setup/SKILL.md" \
  -print -quit 2>/dev/null
```

This cached-file fallback applies to local Claude Code and Codex only. In
Claude Desktop/Cowork, a `SKILL.md` found on the sandbox filesystem is not
evidence that the plugin is installed; the fully qualified `ethos:setup` skill
must be registered by the app itself, and the fix for a missing skill is the
app plugin UI plus a full app restart, not the shell.

The setup skill will:

1. Preserve a working existing CLI or install the latest CLI using the install
   command supplied in the original setup prompt. For direct guide usage, it
   falls back to the production installer. In Claude Desktop/Cowork only, an
   explicit `X-Proxy-Error: blocked-by-allowlist` response makes the CLI an
   optional skipped step; the agent will not retry or bypass the sandbox proxy.
2. When the CLI is available, authenticate and verify it. Fresh Codex setup
   uses one browser approval to provision separate CLI and MCP credentials.
   Temporary approval failures are resumable from the same page and must not
   create a second CLI claim.
3. In Codex, verify the plugin and MCP registration. Run a standalone MCP OAuth
   login only when the CLI was already authenticated and the combined flow did
   not run.
4. Reload Claude Code when needed, or run a fresh ephemeral Codex verification
   process while keeping the original user task open.
5. Call the read-only
   `get_current_ethos_org` tool.

CLI and MCP use separate least-privilege credentials internally. Fresh Codex
setup provisions both from one browser approval. Local Claude Code and Codex
setup is complete only after both CLI and MCP checks pass. Claude Desktop/Cowork
setup is complete when the plugin is enabled and MCP returns the active
organization; if its sandbox proxy blocks the installer, the result must say
that the optional CLI was skipped.

## Reload and finish verification

- **Claude Code:** run `/reload-plugins`, then invoke `/ethos:setup` again in
  the same conversation. If `/reload-plugins` is unavailable (local sessions
  run by the Claude desktop app), start a new conversation and invoke
  `/ethos:setup` there instead — MCP servers load only at session start. If the
  Ethos MCP tool is still missing, have the agent run `claude mcp list`: an
  entry marked `Needs authentication` means finish the MCP OAuth rather than
  reloading; a listed `plugin:ethos:ethos` entry with no Ethos server visible
  in the session means reload/new-conversation again; a missing entry means the
  installed plugin version's MCP config was skipped at parse time, so update
  the marketplace and plugin rather than reloading.
- **Claude Desktop/Cowork:** after installing the plugin in the app UI, fully
  quit and reopen Claude, then invoke `/ethos:setup` in a new conversation.
- **Codex:** stay in the current task. Complete the setup skill's plugin and MCP
  registration checks and its combined authentication flow, then let the skill
  run its read-only ephemeral `codex exec` verification. Do not ask the user to
  create or reopen a task.

If organization policy prevents adding third-party marketplaces or plugins,
report that exact policy blocker. Do not bypass managed settings or install the
plugin by copying files into an unmanaged location.
