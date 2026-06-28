## Ethos Plugin

Remote MCP server and skills for Ethos GTM workflows.

### Preferred Path

Use Ethos MCP first. It is remote, OAuth-backed, and does not require Node, npm, or the Ethos CLI.

### Default MCP Tools

- `find_people` - start natural-language prospect search
- `get_find_people_status` - poll search and resulting table IDs
- `create_csv_upload_handoff` - open browser CSV upload flows
- `get_upload_handoff_status` - poll upload handoff completion
- `source_people_from_company_table` - source people from uploaded company tables
- `create_agent_column` - add an agent-powered column
- `run_table_column` - run sample, selected, empty, count, or all rows
- `enrich_contact_info_sample` - test email/phone enrichment on sample rows
- `enrich_remaining_contact_info` - enrich remaining empty contact-info rows
- `add_leads_to_campaign` - import table rows or contacts into a campaign

### Progressive Discovery

For lower-level operations, call `search_ethos_tools` with the user's intent, then call `call_ethos_tool` with the selected `tool_name` and JSON arguments. Use this for table creation, row/cell edits, columns, agents, lists, and campaign configuration.

### Auth

MCP authorization redirects through normal Ethos login. Access tokens are org-scoped; reconnect to choose a different organization.
