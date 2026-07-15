# Getting started with Ethos

> This guide is written for your coding agent. Give it this link and ask it to
> set Ethos up for you. The agent can install the Ethos plugin and CLI; you only
> need to approve requested commands, finish browser authentication, and reload
> or start a new task when prompted.

Ethos supports Claude Code and Codex through one marketplace plugin. The plugin
bundles Ethos skills and the hosted OAuth-backed MCP server. The setup skill also
installs and authenticates `ethos-cli` so both surfaces are ready.

This runbook is the setup contract for Ethos plugin `0.3.0`. Setup prompts must
link to the immutable `v0.3.0` release tag rather than the mutable default branch.

## Install or update the plugin

Use the section for the agent that is running this guide. Do not ask the user to
open a plugin directory or paste a marketplace URL into application settings.

### Claude Code

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

## Run the setup skill

Continue setup in this session before reloading when possible. Invoke the fully
qualified skill for the current agent:

- Claude Code: `/ethos:setup`
- Codex: `$ethos:setup`

If the newly installed skill is not registered in the current session, locate
the exact installed version from the matching plugin-list command above. Then
use the matching client cache to locate its file and follow it directly as a
runbook. Set `ETHOS_PLUGIN_VERSION` yourself from the command output; do not ask
the user for it.

Claude Code:

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
   falls back to the production installer.
2. Authenticate and verify the CLI, then synchronize Ethos skills and hooks.
3. Reload or start a new task so the plugin MCP server is available.
4. Authenticate MCP separately and call the read-only
   `get_current_ethos_org` tool.

CLI and MCP authentication are separate. Setup is complete only after both
checks pass.

## Reload and finish verification

- **Claude Code:** run `/reload-plugins`, then invoke `/ethos:setup` again in
  the same conversation.
- **Codex:** start a new task, then invoke `$ethos:setup`. A task that was open
  before plugin installation cannot use the new plugin.

If organization policy prevents adding third-party marketplaces or plugins,
report that exact policy blocker. Do not bypass managed settings or install the
plugin by copying files into an unmanaged location.
