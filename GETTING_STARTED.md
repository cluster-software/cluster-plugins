# Getting started with Ethos

> This guide is written for your agent. Follow exactly one branch based on the
> product currently running: Codex, Claude Desktop/Cowork, or claude.ai in the
> browser. If no branch matches, stop and tell the user which product you are
> running in.

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

## Claude Desktop/Cowork

Claude Desktop/Cowork cannot install the Ethos plugin or configure its MCP
server from the agent session. Do not run marketplace, plugin, CLI, or MCP setup
commands. Give the user these manual steps instead:

1. Open **Claude Desktop → Customize → Plugins**.
2. Select **Add marketplace** and enter `cluster-software/cluster-plugins`.
3. Find **Ethos** in the marketplace and select **Install**.
4. Open **Customize → Plugins → Connectors**, find **Ethos**, and select
   **Install**.
5. Approve access in the browser.

Watch the installation walkthrough:
[Install Ethos in Claude Desktop](https://www.loom.com/embed/ae9f539200d04947acccb0e2e1086b6c)

Stop after presenting these instructions.

## claude.ai in the browser

claude.ai uses Ethos through the hosted Ethos MCP server, added as a custom
connector. Do not install ethos-cli: the sandbox cannot reach the installer
and is discarded after the session. Give the user these manual steps instead:

1. Open **Settings → Connectors** and select **Add custom connector**.
2. Enter **Ethos** as the name and `https://api.ethos.hello-cluster.com/mcp`
   as the URL, then select **Add**.
3. Connect the Ethos connector and approve access when prompted.

On Team and Enterprise plans, only workspace Owners can add custom connectors.
If the option is missing, ask an Owner to add the same URL in
**Organization settings → Connectors**, then enable it yourself under
**Settings → Connectors**.

Stop after presenting these instructions.
