---
name: find-people
description: Find prospects from a natural-language ICP using Ethos MCP.
catalog_title: Find people
catalog_category: Prospecting
catalog_description: Find relevant prospects from scratch with a natural-language ICP. Ethos creates linked company and people tables in the background.
---

# Find People

Use Ethos MCP first.

1. Call `find_people` with a specific query that includes both target companies and target people. Queries naming specific employers run against exactly those companies when they resolve.
2. If the response status is `needs_refinement` with no `search_id`, the query was declined before a search started. Follow the response `next_action`: either rewrite the query to describe both companies and people, or pivot to `create_table` (entity_type `company`, one row per company in `data.company_names`) plus `source_people_from_company_table`. Do not retry the same query.
3. Otherwise call `get_find_people_status` until the job succeeds, fails, or needs refinement.
4. Return the `people_table_id`, table URL, counts, and any refinement suggestions.

For an empty company table that will be populated by a workflow, call
`source_people_from_company_table` with `create_only: true`. Retain the returned
`column_id` in the workflow configuration so the workflow can run that column
after the rows exist. When qualification is represented by a boolean or other
prior column, pass a column-level `run_condition`; non-matching rows are recorded
as skipped and spend no People Finder credits. Use `filters` only to define the
source table scope, not as a substitute for conditional workflow execution. This
mode creates the People Finder column without sourcing people or spending run
credits; omit `create_only` when contacts should be sourced immediately. For
company-scoped signal sourcing, follow the contract in `CLAUDE.md`: use
`scope="all"`, include the targeting brief, and pass `source_column_ids` for
signal fields that must be preserved on the resulting people.

If MCP tools are unavailable, ask the user to reconnect Ethos MCP or install the Ethos plugin.

Keep responses concise: IDs, URLs, counts, status, and the next action.
