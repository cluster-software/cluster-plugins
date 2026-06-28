---
name: find-people
description: Find prospects from a natural-language ICP using Ethos MCP.
---

# Find People

Use Ethos MCP first.

1. Call `find_people` with a specific query that includes both target companies and target people.
2. Call `get_find_people_status` until the job succeeds, fails, or needs refinement.
3. Return the `people_table_id`, table URL, counts, and any refinement suggestions.

If MCP tools are unavailable, fall back to the Ethos CLI when installed. If neither is available, ask the user to install the Ethos plugin or connect Ethos MCP.

Keep responses concise: IDs, URLs, counts, status, and the next action.
