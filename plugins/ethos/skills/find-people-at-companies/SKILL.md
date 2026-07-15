---
name: find-people-at-companies
description: Upload a company CSV and source people from it using Ethos MCP.
catalog_title: Find people at companies
catalog_category: Prospecting
catalog_description: Upload or reuse a company list, define the target personas and buying signals, then source the right contacts at each account.
---

# Find People At Companies

Use Ethos MCP first.

1. Reuse an existing upload handoff token if one is already present in the conversation.
2. Otherwise call `create_csv_upload_handoff` with `flow: "find-people-at-companies"`.
3. Have the user open the handoff URL and upload the company CSV.
4. Poll `get_upload_handoff_status` until it returns a `result_table_id`.
5. Inspect the table if column or view IDs are needed, using `search_ethos_tools` for `inspect table`.
6. Summarize the detected table, company identifiers, and targeting brief, then ask for confirmation before starting people sourcing.
7. After confirmation, call `source_people_from_company_table` with the company table, saved view, input column IDs, and targeting brief.
8. Poll `inspect_table_summary` on the company table until `recent_runs` shows the sourcing run with a terminal status. If the run failed outright, report the failure instead of polling further.
9. Once cells have succeeded, call `create_people_table` on the company table to materialize the linked people table. Run `enrich_contact_info` and campaign steps against that people table id, never the company table.

Do not ask the user to install npm or the CLI on the MCP-first path.
