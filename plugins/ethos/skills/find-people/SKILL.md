---
name: find-people
description: Find prospects from a natural-language ICP using Ethos MCP.
---

# Find People

Use Ethos MCP first.

1. Call `find_people` with a specific query that includes both target companies and target people. Queries naming specific employers run against exactly those companies when they resolve.
2. If the response status is `needs_refinement` with no `search_id`, the query was declined before a search started. Follow the response `next_action`: either rewrite the query to describe both companies and people, or pivot to `create_table` (entity_type `company`, one row per company in `data.company_names`) plus `source_people_from_company_table`. Do not retry the same query.
3. Otherwise call `get_find_people_status` until the job succeeds, fails, or needs refinement.
4. Return the `people_table_id`, table URL, counts, and any refinement suggestions.

If MCP tools are unavailable, ask the user to reconnect Ethos MCP or install the Ethos plugin.

Keep responses concise: IDs, URLs, counts, status, and the next action.
