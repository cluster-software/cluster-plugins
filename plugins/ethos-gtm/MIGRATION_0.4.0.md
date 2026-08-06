# Ethos plugin 0.4.0 migration

Ethos 0.4.0 replaces the previous atomic/discovery MCP catalog with 18 direct
intent tools and two skill fallbacks. The MCP URL is unchanged.

## Required user action

1. Update the Ethos plugin to `0.4.0`.
2. Keep exactly one authenticated Ethos MCP registration pointing to
   `https://api.ethos.hello-cluster.com/mcp`.
3. Disconnect/reconnect that registration if the client still shows old tools.
4. Discard active Ethos chats/tasks and start a fresh one; clients cache tool
   schemas per session.

Normal natural-language prompts do not need to change. Custom prompts and
automations must use the new names in the mapping below.

## Custom automation contract

- Pass a fresh `idempotency_key` to every mutating intent tool whose schema
  requires one. Reuse that key only for an exact retry of the same logical
  operation. A quote-approval retry keeps the same arguments and key while
  adding the returned `quote_id`; a new selection, configuration, or state
  transition needs a new key.
- When an asynchronous tool returns `working`, call `get_job_status` with its
  returned job and a suitable `wait_seconds` value. Repeat only while the job
  remains nonterminal; do not call a retired per-domain status tool.

## Client refresh

- Claude Desktop/Cowork: use the organization-managed `ethos` connector, then
  start a new chat/task.
- Standalone Claude Code: update the plugin, authenticate its MCP server, and
  start a new session.
- Claude Code inside Desktop: keep only the registration supported by that
  surface active. If the managed connector cannot be disabled, disable the
  duplicate plugin server; plugin skills can use the managed connector.
- Codex: upgrade the `cluster-plugins` marketplace, reinstall/update
  `ethos-gtm`, authenticate its MCP server, and start a new task.

Never leave two active registrations pointing to the same Ethos endpoint.

| Previous operation | 0.4.0 tool |
| --- | --- |
| list/get current org and workspace context | `get_workspace_overview` |
| switch org | `switch_ethos_org` |
| find people, search import, CSV handoff, source from companies | `find_people` |
| pull a supported signal | `source_signal` |
| inspect/list table rows and metadata | `inspect_table` |
| create/run an agent column | `enrich_table` |
| contact-info enrichment | `enrich_contact_info` |
| any per-domain status tool | `get_job_status` |
| campaign list/detail/performance/cohorts | `analyze_campaigns` |
| list/campaign/sequence draft creation | `build_campaign_draft` |
| add leads, replace sequence, update settings | `update_campaign` |
| launch, pause, resume campaign | `set_campaign_state` |
| list/search inbox conversations | `search_conversations` |
| read a merged conversation | `get_conversation` |
| send an inbox message | `send_reply` |
| list/read workflows and runs | `get_workflow_overview` |
| create/update a draft or paused workflow | `configure_workflow` |
| activate/pause workflow | `set_workflow_state` |
| resource fallback discovery/load | `list_ethos_skills`, `load_ethos_skill` |

`search_ethos_tools`, `call_ethos_tool`, `list_default_ethos_tools`,
`load_ethos_skill_resource`, old atomic tools, and old per-job status names no
longer exist. Unsupported administration remains in the Ethos UI/API.
