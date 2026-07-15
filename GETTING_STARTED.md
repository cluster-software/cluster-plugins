# Getting started with Ethos

> This guide is written for your coding agent. Give it this link and ask it to
> set Ethos up for you. The agent can install the Ethos plugin and, where the
> host allows it, the CLI; you only need to approve requested commands, finish
> browser authentication, and reload Claude when prompted.

Ethos supports Claude and Codex through one marketplace plugin. The plugin
bundles Ethos skills and the hosted OAuth-backed MCP server. Local Claude Code
and Codex setup also installs and authenticates `ethos-cli`. In Claude
Desktop/Cowork, the plugin and MCP connection are required; the CLI is optional
because the sandbox proxy may block its installer.

This runbook is maintained alongside the marketplace. The commands below resolve
the current Ethos plugin version from marketplace metadata.

## Install or update the plugin

Use the section for the agent that is running this guide. Do not ask the user to
open a plugin directory or paste a marketplace URL into application settings.

### Claude (Claude Code and Desktop/Cowork)

Inspect the configured marketplaces and installed plugins first:

```bash
claude plugin marketplace list
claude plugin list --json
```

If `cluster-plugins` is missing, add it. Otherwise update it:

```bash
claude plugin marketplace add cluster-software/cluster-plugins
claude plugin marketplace update cluster-plugins
```

If `ethos@cluster-plugins` is missing, install it. Otherwise update it:

```bash
claude plugin install ethos@cluster-plugins
claude plugin update ethos@cluster-plugins
```

These commands install to user scope by default.

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

Claude:

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

- **Claude:** run `/reload-plugins`, then invoke `/ethos:setup` again in the
  same conversation. If Claude Desktop/Cowork requires an app-level reload,
  fully quit and reopen Claude, then invoke the skill again.
- **Codex:** stay in the current task. Complete the setup skill's plugin and MCP
  registration checks and its combined authentication flow, then let the skill
  run its read-only ephemeral `codex exec` verification. Do not ask the user to
  create or reopen a task.

If organization policy prevents adding third-party marketplaces or plugins,
report that exact policy blocker. Do not bypass managed settings or install the
plugin by copying files into an unmanaged location.
