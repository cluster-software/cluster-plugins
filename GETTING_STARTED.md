# Getting started with Ethos

> Follow exactly one branch based on the
> product currently running: Codex or Claude (desktop, cowork, claude.ai).

## Codex

Complete setup for the user. Do not merely explain these steps or ask the user
to install the marketplace through the UI.

### 1. Install or update the plugin

Inspect the current state:

```bash
codex plugin marketplace list
codex plugin list --available --json
```

Add the Cluster marketplace when it is missing; otherwise upgrade it:

```bash
codex plugin marketplace add cluster-software/cluster-plugins
codex plugin marketplace upgrade cluster-plugins
```

Install or refresh Ethos:

```bash
codex plugin add ethos@cluster-plugins --json
```

### 2. Run the setup skill

Invoke `$ethos:setup` in this task. If the newly installed skill is not yet
registered, read the exact installed version from the plugin JSON, locate its
cached runbook, and follow it directly:

```bash
ETHOS_PLUGIN_VERSION='<installed version from codex plugin add/list JSON>'
find "${CODEX_HOME:-$HOME/.codex}" \
  -type f -path "*/plugins/cache/*/ethos/${ETHOS_PLUGIN_VERSION}/skills/setup/SKILL.md" \
  -print -quit 2>/dev/null
```

The setup skill installs and authenticates `ethos-cli`, verifies that the
plugin and hosted MCP server are enabled, completes MCP OAuth, and calls the
read-only `get_current_ethos_org` tool. Keep the user in this task throughout
setup.

### 3. Give the user next steps

After setup returns the active Ethos organization, tell the user Ethos is ready
and suggest this skill:

- `$ethos:find-people` — find prospects from a natural-language ICP.

## Claude

Claude Desktop/Cowork and claude.ai cannot install the Ethos plugin or
configure its MCP server from the agent session. Do not run marketplace,
plugin, CLI, or MCP setup commands. Give the user these manual steps instead:

1. Open **Claude → Customize → Plugins**.
2. Select **Add marketplace** and enter `cluster-software/cluster-plugins`.
3. Find **Ethos** in the marketplace and select **Install**.
4. Open **Customize → Plugins → Connectors**, find **Ethos**, and select
   **Install**.
5. Approve access in the browser.

Watch the installation walkthrough:
[Install Ethos in Claude Desktop](https://www.loom.com/embed/ae9f539200d04947acccb0e2e1086b6c)

Stop after presenting these instructions. The user must complete the Claude
UI flow themselves.
