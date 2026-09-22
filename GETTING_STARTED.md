# Getting started with Cluster

Cluster was formerly known as Ethos. Both names refer to the same product and
hosted MCP server, now displayed as **GTM Cluster**. Existing plugin identifiers,
MCP registrations, and the hosted URL retain their `ethos` names, so reuse an
existing connection rather than creating a duplicate.

> Follow exactly one branch for the product running this session: Claude,
> ChatGPT web, or Codex. Cluster uses one hosted OAuth-backed MCP server. Do not
> configure a second server at the same URL.

## Claude

Claude chat, Desktop, and Cowork cannot complete their own plugin installation
from an agent conversation. Present these steps to the user and stop so they can
finish the UI flow:

1. Open **Customize → Plugins**.
2. Select **Add marketplace** and enter `cluster-software/cluster-plugins`.
3. Find **ethos** (Cluster) in the marketplace and install or update it to **0.7.2**.
4. Open **Customize → Plugins → Connectors**. If Cluster is already connected,
   keep that connector and do not add or authenticate another Cluster server.
   Otherwise, find the existing **ethos** / **GTM Cluster** connector, select
   **Install**, and approve access in the browser.
5. Start a new chat so Claude loads the current MCP tools and resources.
6. Ask: `Use Cluster to confirm the active organization.` The connection is ready
   when the read-only `get_current_ethos_org` operation returns the active
   organization.

Watch the installation walkthrough:
[Install Cluster in Claude Desktop](https://www.loom.com/embed/ae9f539200d04947acccb0e2e1086b6c)

## ChatGPT web

In ChatGPT in a web browser, present these steps to the user and let them
complete the connection in the UI. If Cluster is already connected, reuse that
connection and skip to step 4.

1. Open **Settings → Security and login** and enable **Developer mode**.
   If it is unavailable, explain that account or workspace policy may restrict
   it and offer the Claude or Codex setup path.
2. Open [ChatGPT Plugins](https://chatgpt.com/plugins), select the **plus**
   button, and name the connection **Cluster**.
3. Enter `https://api.ethos.hello-cluster.com/mcp` as the MCP server URL,
   choose OAuth authentication, and create the connection. Approve access to
   the intended Cluster workspace in the authorization flow.
4. Start a **new ChatGPT conversation** and select Cluster from the tools menu.
5. Ask: `Use Cluster to confirm the active organization.` The connection is ready
   when the read-only `get_current_ethos_org` operation returns the active
   organization.

See [OpenAI's connection guide](https://developers.openai.com/plugins/deploy/connect-chatgpt)
for the current UI flow and availability requirements.

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

Require version `0.7.2` and an enabled `ethos-gtm@cluster-plugins` installation.
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

Have the user approve access in the browser if authorization is required.

### 3. Hand off to a new Codex task

Once installation and OAuth are complete, give the user this handoff and stop.
Keep **new Codex task** bold in your response so the required next step is clear:

> Cluster is installed and authorized. Start a **new Codex task** and paste:
>
> `Use Cluster to confirm the active organization.`

The new task loads the current MCP tools and resources. Do not ask the user to
paste the installation prompt again or repeat installation because tools are
unavailable in the original task.

In the new task, the connection is ready when the read-only
`get_current_ethos_org` operation returns the expected active organization. This
check does not read recent workspace objects. Use `get_workspace_overview` when
saved GTM context or recent objects are also needed. Cluster exposes its complete
granular tool catalog directly; Codex uses native progressive discovery to load
the operations required for each request.

If the operation is unavailable, recheck the plugin version, the canonical MCP
registration, and OAuth. Do not add another Cluster server.

## Analytics

Ask Cluster to compare outreach by campaign, user, sender, and channel.
`get_analytics_schema` describes metrics, formulas, supported dimensions, and
filter options. `query_analytics` combines groupings and AND/OR filters, compares
periods, and returns cohort-rate components, coverage, and an app link.

Use `list_analytics_records` to inspect contributors, retaining the query and
adding group constraints to `scope`. Rates can expose either numerator or
denominator. `export_analytics` returns CSV for up to 10,000 groups. Saved reports
have separate list, get, create, update, and delete tools.

Activity counts use event dates; conversion rates include subsequent outcomes
up to now for the reached cohort, with no time limit after outreach. Report
incomplete classification. Omit the retired `observation_days` query setting.
Sending-user grouping uses explicit ownership assignments; use
`assign_analytics_sender_owner` only for confirmed ownership. All tools honor
the active workspace. These capabilities require the corresponding backend deployment.
