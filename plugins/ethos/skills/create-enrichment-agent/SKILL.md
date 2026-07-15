---
name: create-enrichment-agent
description: Add and run an Ethos agent column through MCP.
catalog_title: Create enrichment agent
catalog_category: Enrichment
catalog_description: Create company, person, or people-sourcing agents and wire them into table columns with structured outputs.
---

# Create Enrichment Agent

Use Ethos MCP first.

1. Identify the table and input columns.
2. Call `create_agent_column` with a clear column name, prompt, output fields, and input column IDs.
3. Call `run_table_column` with `scope: "first_5"` unless the user explicitly wants a broader run.
4. After sample validation, call `run_table_column` with `scope: "empty"`, `count`, `all`, targeted `row_ids`, or `lower_range`/`upper_range` for a 1-based inclusive displayed-row batch.

For lower-level table or agent configuration, discover atomic tools with `search_ethos_tools`, then use `call_ethos_tool`.
