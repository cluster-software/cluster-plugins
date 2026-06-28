---
name: find-people-at-companies
description: Upload a company CSV and source people from it using Ethos MCP.
---

# Find People At Companies

Use Ethos MCP first.

1. Reuse an existing upload handoff token if one is already present in the conversation.
2. Otherwise call `create_csv_upload_handoff` with `flow: "find-people-at-companies"`.
3. Have the user open the handoff URL and upload the company CSV.
4. Poll `get_upload_handoff_status` until it returns a `result_table_id`.
5. Inspect the table if column or view IDs are needed, using `search_ethos_tools` for `inspect table`.
6. Call `source_people_from_company_table` with the company table, saved view, input column IDs, and targeting brief.

Do not ask the user to install npm or the CLI on the MCP-first path.
