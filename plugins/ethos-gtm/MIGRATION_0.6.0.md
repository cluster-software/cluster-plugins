# Migrating to Ethos 0.6.0

Ethos 0.6.0 restores the granular MCP tools as the canonical capability
surface. The MCP server exposes all atomic operations directly, plus the
read-only `get_workspace_overview` orientation tool. Intent tools,
server-side tool-search/dispatch wrappers, job wrappers, and fallback skill
loader tools are no longer part of the surface.

The plugin skills are complete playbooks that compose direct granular tools;
they are not alternate APIs or hidden workflows. Power users can call any
granular tool directly, and clients with native Tool Search can progressively
discover the same public tool catalogue.

The surface contains 74 tools on the current platform: the planned 72 restored
granular tools, `get_workspace_overview`, and the subsequently added atomic
`exclude_campaign_leads` capability. The richer cross-campaign lead search is
available through the existing `list_campaign_leads` tool.

## Upgrade

1. Update the Ethos plugin to 0.6.0.
2. Reconnect or refresh the existing Ethos MCP server if the client requests
   it. Do not add a second registration.
3. Start a new task or chat. Existing sessions may cache the previous tool and
   skill schemas.

## Common mappings

| Previous intent tool | Granular replacement |
| --- | --- |
| `analyze_campaigns` | `list_campaigns`, `get_campaign`, `get_campaign_performance`, `list_campaign_leads` |
| `build_campaign_draft` | `create_list`, `generate_campaign_copy`, `create_campaign_with_sequence`, `add_leads_to_campaign` |
| `update_campaign` | `add_leads_to_campaign`, `update_campaign_sequence`, `update_campaign_settings` |
| `search_campaign_leads` | `list_campaign_leads` with campaign, status, identity, or conversation filters |
| `update_campaign` with `exclude_leads` | `exclude_campaign_leads` |
| `set_campaign_state` | `launch_campaign`, `pause_campaign`, `resume_campaign` |
| `inspect_table` | `list_tables`, `inspect_table_summary`, `get_column` |
| `enrich_table` | `create_agent_column`, `run_table_column`, `get_column_run_status` |
| broad `find_people` modes | `find_people`, `create_salesnav_import`, `create_csv_upload_handoff`, or `source_people_from_company_table` |
| `source_signal` | `list_signal_definitions`, `pull_signal`, `get_signal_pull_status` |
| `search_conversations` / `get_conversation` / `send_reply` | `list_unibox_conversations`, `get_unibox_conversation`, `send_unibox_message` |
| `configure_workflow` / `set_workflow_state` | `create_workflow`, `update_workflow`, `activate_workflow`, `pause_workflow`, `archive_workflow` |
| `get_job_status` | the operation-specific blocking status tool returned by the starter call |

Use `get_workspace_overview` once at the start of a task when organization or
workspace context is needed. Use the resource-specific list/get tools for the
authoritative details after that.
