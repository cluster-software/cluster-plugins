# Getting started with Ethos

> Follow exactly one branch for the product running this session: Claude or
> Codex. Ethos uses one hosted OAuth-backed MCP server. Do not configure a
> second server at the same URL.

## Claude

Claude chat, Desktop, and Cowork cannot complete their own plugin installation
from an agent conversation. Present these steps to the user and stop so they can
finish the UI flow:

1. Open **Customize → Plugins**.
2. Select **Add marketplace** and enter `cluster-software/cluster-plugins`.
3. Find **Ethos** in the marketplace and install or update it to **0.7.0**.
4. Open **Customize → Plugins → Connectors**. If Ethos is already connected,
   keep that connector and do not add or authenticate another Ethos server.
   Otherwise, find **Ethos**, select **Install**, and approve access in the
   browser.
5. Start a new chat so Claude loads the current MCP tools and resources.
6. Ask: `Use Ethos to show me the active workspace.` The connection is ready
   when the read-only `get_workspace_overview` operation returns the active
   organization.

Watch the installation walkthrough:
[Install Ethos in Claude Desktop](https://www.loom.com/embed/ae9f539200d04947acccb0e2e1086b6c)

## Codex

Complete the installation for the user rather than asking them to use the UI.

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

If `codex plugin list --json` reports the retired `ethos@cluster-plugins`
identity as installed, remove only that identity:

```bash
codex plugin remove ethos@cluster-plugins
```

Install or refresh the current plugin:

```bash
codex plugin add ethos-gtm@cluster-plugins --json
```

Require version `0.7.0` and an enabled `ethos-gtm@cluster-plugins` installation.
The marketplace authentication policy should open MCP OAuth during installation.

### 2. Verify the hosted MCP connection

Inspect registrations:

```bash
codex mcp list --json
codex mcp get gtm_ethos --json
```

Require exactly one enabled registration for
`https://api.ethos.hello-cluster.com/mcp`. The canonical registration is
`gtm_ethos`. If the retired `ethos_gtm` registration is also enabled at that
exact URL, remove only the retired registration and inspect the list again:

```bash
codex mcp remove ethos_gtm
codex mcp list --json
```

Do not remove a differently named registration or one with a different URL;
report it for manual review. If the canonical server still needs authorization,
run:

```bash
codex mcp login gtm_ethos
```

Approve access in the browser, then start a new task so Codex loads the current
MCP tools and resources.

### 3. Confirm workspace access

In the new task, ask: `Use Ethos to show me the active workspace.` The
connection is ready when the read-only `get_workspace_overview` operation
returns the active organization, saved GTM context, and recent workspace
objects. Ethos exposes its complete granular tool catalog directly; Codex uses
native progressive discovery to load the operations required for each request.

If the operation is unavailable, recheck the plugin version, the canonical MCP
registration, and OAuth. Do not add another Ethos server.
