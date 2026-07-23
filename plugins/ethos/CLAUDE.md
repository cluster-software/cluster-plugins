## Ethos Plugin

Remote MCP server and skills for Ethos GTM workflows.

### Preferred Path

Use Ethos MCP first. It is remote, OAuth-backed, and does not require Node, npm, or the Ethos CLI.

### Default MCP Tools

- `find_people` - start natural-language prospect search
- `get_find_people_status` - poll search and resulting table IDs
- `list_ethos_orgs` - list organizations authorized for this MCP connection
- `get_current_ethos_org` - show the active organization
- `switch_ethos_org` - switch to another authorized organization
- `create_csv_upload_handoff` - open browser CSV upload flows
- `get_upload_handoff_status` - poll upload handoff completion
- `source_people_from_company_table` - source people from uploaded company tables
- `create_people_table` - materialize sourced people and retain selected exact-row company fields
- `list_signal_definitions` - list built-in and org-scoped custom signals with their config and row schemas
- `pull_signal` - run a sourceable signal and land its matches in an Ethos table
- `get_signal_pull_status` - wait server-side for a signal pull and return its table and row count
- `create_workflow` - create a recurring signal workflow
- `create_agent_column` - add an agent-powered column
- `run_table_column` - run first_5, selected row_ids, empty, count, or all rows
- `enrich_contact_info` - enrich contact info for first_5, selected row_ids, empty, count, or all rows
- `add_leads_to_campaign` - import table rows or contacts into a campaign
- `populate_column_from_table` - preview or copy values across related tables by ordered match keys
- `extract_json_columns` - flatten a structured/JSON agent column into linked flat columns on the same table

### Progressive Discovery

For lower-level operations, call `search_ethos_tools` with the user's intent, then call `call_ethos_tool` with the selected `tool_name` and JSON arguments. Use this for table creation, single or bulk cell edits, columns, agents, lists, and campaign configuration.

The full LinkedIn, email, and mixed campaign lifecycle is searchable: `list_campaigns`, `get_campaign`, `create_list`, `generate_campaign_copy`, `search_copy_bank`, `create_campaign_with_sequence`, `attach_list_to_campaign`, and `launch_campaign` (destructive - starts real sends). See the `create-campaign` skill for the end-to-end playbook.

The cross-channel unibox is also searchable: `list_unibox_conversations`, `get_unibox_conversation`, and `send_unibox_message` (destructive - sends a real reply and stops pending automation for that contact). Campaign conversations are the default; use `include_all=true` only when the user explicitly asks for organic account conversations. See the `manage-unibox` skill for safe pagination, thread selection, and idempotent retries.

### Custom Signals

`list_signal_definitions` includes only the custom signals assigned to the active organization. They use keys such as `custom:<assignment-id>` and report `configuration_mode: "managed"`. Pass `config={}` to `pull_signal` and an empty `trigger_config` to `create_workflow`; customers and agents do not override managed configuration.

After `pull_signal`, call `get_signal_pull_status` with `wait_seconds` in the 15-180 second range for work that normally takes minutes. A successful pull with zero rows and no table is a normal no-match result. Do not substitute another signal, infer or select its Lambda/Daytona executor, or retry through a different executor after failure. The executor is an internal deployment detail and the returned table is the stable integration surface.

Person-scoped signals return the people table to use downstream. Company-scoped signals return a company table: inspect its columns, run `source_people_from_company_table` with any needed `filters`, `scope="all"`, and a targeting brief, wait for the run to finish, then call `create_people_table`. Pass `source_column_ids` for non-identity signal fields needed downstream; Ethos copies them from each exact source company row onto its linked people, preserving signal context without reimplementing enrichment inside the custom signal.

The CLI exposes the same assignments through `ethos signals list`, `ethos signals pull <custom:key>`, `ethos signals pull-status <job-id>`, and the normal `ethos workflows` commands. Omit `--config` for managed custom signals. For a company-scoped result, use `ethos tables source-people` followed by `ethos tables create-people-table --source-column <id>` for each signal-context column to retain.

### Organization Context

MCP authorization redirects through normal Ethos login. If the user authorized multiple organizations, call `list_ethos_orgs` or `get_current_ethos_org` when org context matters, and call `switch_ethos_org` before creating or modifying resources in another authorized organization.
