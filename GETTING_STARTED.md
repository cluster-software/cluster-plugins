# Getting started with Ethos

> Follow exactly one branch based on the
> product currently running: Claude (including desktop, cowork, claude.ai) or Codex.

## Claude (chat app, desktop, cowork)

Claude chat app, desktop, cowork cannot install the Ethos plugin or
configure its MCP server from the agent session. Print these steps verbatim. Do not try
to execute anything yourself. The user has to do this manually.

Print:
```
1. Open **Customize → Plugins**.
2. Select **Add marketplace** and enter `cluster-software/cluster-plugins`.
3. Find **Ethos** in the marketplace and install or update it to **0.6.1**.
4. Open **Customize → Plugins → Connectors**. If Ethos is already connected,
   keep that connector and do not add or authenticate another Ethos server.
   Otherwise, find **Ethos**, select **Install**, and approve access in the
   browser.
5. Start a new chat so Claude loads the current tool and skill schemas.

Watch the installation walkthrough:
[Install Ethos in Claude Desktop](https://www.loom.com/embed/ae9f539200d04947acccb0e2e1086b6c)
```

Stop after presenting these instructions. The user must complete the Claude
UI flow themselves.


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

Remove the legacy Codex plugin identity when `codex plugin list --json` reports
`ethos@cluster-plugins` as installed:

```bash
codex plugin remove ethos@cluster-plugins
```

Install or refresh Ethos GTM:

```bash
codex plugin add ethos-gtm@cluster-plugins --json
```

The expected release is `0.6.1`. Start a new task after setup so Codex discards
cached skill and tool schemas.

### 2. Run the setup skill

Invoke `$ethos-gtm:setup` in this task. If the newly installed skill is not yet
registered, read the exact installed version from the plugin JSON, locate its
cached runbook, and follow it directly:

```bash
ETHOS_PLUGIN_VERSION='<installed version from codex plugin add/list JSON>'
find "${CODEX_HOME:-$HOME/.codex}" \
  -type f -path "*/plugins/cache/*/ethos-gtm/${ETHOS_PLUGIN_VERSION}/skills/setup/SKILL.md" \
  -print -quit 2>/dev/null
```

The setup skill installs and authenticates `ethos-cli`, verifies that exactly
one hosted Ethos MCP registration is enabled, completes MCP OAuth, and calls the
read-only `get_workspace_overview` tool. Keep the user in this task throughout
setup.

### 3. Give the user next steps

After setup returns the active Ethos organization, tell the user Ethos is ready
and suggest this skill:

- `$ethos-gtm:find-people` — find prospects from a natural-language ICP.
- `$ethos-gtm:source-social-audience` — source a competitor's LinkedIn or X
  followers into a people table.
