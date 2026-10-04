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
3. Find **ethos** (Cluster) in the marketplace and install or update it to **0.8.2**.
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

Require version `0.8.2` and an enabled `ethos-gtm@cluster-plugins` installation.
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

## Fast workspace discovery

Use `list_tables`, `list_lists`, and `list_campaigns` to discover resources.
These tools return bounded summary pages without loading table cells, recipient
records, or sending history. Pass `search` to resolve names on the server;
`list_campaigns` also accepts `status`. Each response includes `data.page` with
`has_more` and `next_offset`. Pass that offset with the same search/filter to
continue only when more results are needed. List summaries include contact
counts, so counting recipients does not require `get_list`.

Request detail tools only after choosing the relevant resource. The hosted
server exposes the current tool schemas directly; reconnect if a client has
cached an older schema.

## Human calling with Cluster Dialer

Cluster Dialer is a sequence channel alongside LinkedIn and email. The human
speaks on each call; the agent initiates and controls it through Cluster.
Availability depends on calling being enabled for the workspace.

1. Use `get_dialer_readiness` for setup status, the dashboard URL, and credit prices.
2. Use `list_dialer_numbers`. After explicit approval of the recurring monthly
   credit price, `purchase_dialer_number` can acquire a number. Keep its
   `request_key` unchanged when retrying. `release_dialer_number` stops renewal.
3. For desktop and terminal agents, use the local **Cluster Audio** companion
   on the human's computer. With explicit microphone consent, call hosted
   `create_dialer_audio_session` and pass its capability directly to local
   `connect_cluster_microphone`. Wait for `state=ready`.
   `list_dialer_audio_sessions` returns the same connected session. No dashboard
   tab is required. The dashboard microphone remains available for web clients.
4. Use `list_dialer_tasks` for due sequence calls, or call a contact or phone number
   directly. `start_dialer_call` requires exactly one of `contact_id` or `phone`,
   plus the calling number, connected session, stable request key and approved
   maximum credit cost. US phone numbers can omit +1; other countries need their
   country code. Direct phone calls do not create contacts. Sequence calls require
   `contact_id` and the due task's `step_run_id`.
5. Use `control_dialer_call` to mute, unmute, or request hangup.
   `get_dialer_call_status(wait_seconds=15)` waits for completion; increase to
   180 seconds for a longer call. `list_dialer_calls` shows recent history.
6. For sequence calls, use `record_dialer_outcome` to save the result and continue
   the sequence. Ordinary calls are logged automatically without an outcome step.
   You can still record notes or set `stop_outreach=true` when someone opts out.

The dashboard is under **Settings → Dialer**. Enter a phone number and select
**Call** to connect the browser microphone and place the call. Calling numbers
and recent call logs are on the same page.

Call costs reserve a maximum and settle against verified duration. Unused
reserved credits are refunded. Never retry an uncertain operation with a new
request key, switch providers, or treat a disconnected microphone as permission
to place a new call. Open the existing call status instead. For custom audio
clients, `create_dialer_audio_session` issues a short-lived connection capability;
never publish that capability or persist it in shared documents.


### Native microphone setup for desktop and terminal agents

Cluster Audio is an optional local MCP server alongside the existing hosted
Cluster connection. It opens the microphone and speakers on the human's computer;
installing it in a remote development workspace cannot access the laptop's audio.
The hosted connection still owns authentication, contacts, calls, and billing.

Install the companion from the feature checkout on the human's computer using
`uv tool install ./cluster-audio`. The companion is not yet published to a public
registry. Use the [companion source and installation guide](https://github.com/cluster-software/ethos/tree/codex/cluster-dialer/cluster-audio)
for the reviewed source, platform requirements, and test gateway configuration.
It needs no provider credentials or additional API key.

Add the installed executable as a local stdio MCP server named `cluster_audio`.
Use its absolute path. For Codex:

```sh
codex mcp add cluster_audio -- /absolute/path/to/cluster-audio mcp
```

For Claude Code:

```sh
claude mcp add --transport stdio --scope user cluster_audio -- /absolute/path/to/cluster-audio mcp
```

For Claude Desktop, merge this into its local MCP configuration:

```json
{
  "mcpServers": {
    "cluster_audio": {
      "command": "/absolute/path/to/cluster-audio",
      "args": ["mcp"]
    }
  }
}
```

Reload the client's MCP connections. The four local tools are
`list_cluster_audio_devices`, `connect_cluster_microphone`,
`get_cluster_microphone_status`, and `disconnect_cluster_microphone`.
On macOS, allow the hosting application under System Settings → Privacy &
Security → Microphone when prompted. Use headphones; native acoustic echo
cancellation is not included. Capture stops automatically after the call or
two idle minutes, and on device/network failure. Explicit disconnect also
requests hangup. Do not leave capture open after the user cancels.

Example: “Enable my microphone using Cluster Audio; I approve microphone access.
Call my selected contact through Cluster for at most one minute and three credits.
I will speak on the call.” Check the current configured credit price first.

The hosted MCP must have the dialer feature deployed, or use a separate test
backend connection before merge. Never switch a test call to the production
connection silently. Clients that only support remote connectors cannot launch
the native companion; explain that limitation rather than claiming their
built-in dictation microphone is available to an MCP tool.
