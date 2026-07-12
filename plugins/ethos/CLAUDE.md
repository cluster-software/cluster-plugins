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
- `create_agent_column` - add an agent-powered column
- `run_table_column` - run first_5, selected row_ids, empty, count, or all rows
- `enrich_contact_info` - enrich contact info for first_5, selected row_ids, empty, count, or all rows
- `add_leads_to_campaign` - import table rows or contacts into a campaign

### Progressive Discovery

For lower-level operations, call `search_ethos_tools` with the user's intent, then call `call_ethos_tool` with the selected `tool_name` and JSON arguments. Use this for table creation, row/cell edits, columns, agents, lists, and campaign configuration.

The full LinkedIn, email, and mixed campaign lifecycle is searchable: `list_campaigns`, `get_campaign`, `create_list`, `generate_campaign_copy`, `search_copy_bank`, `create_campaign_with_sequence`, `attach_list_to_campaign`, and `launch_campaign` (destructive - starts real sends). See the `create-campaign` skill for the end-to-end playbook.

### Organization Context

MCP authorization redirects through normal Ethos login. If the user authorized multiple organizations, call `list_ethos_orgs` or `get_current_ethos_org` when org context matters, and call `switch_ethos_org` before creating or modifying resources in another authorized organization.
