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

## Credit approval

`run_table_column` spends org credits per billable row. A validated sample is necessary but
not sufficient for the full run — the user also approves the spend:

1. Call `run_table_column` with `dry_run: true` and the intended full scope to get
   `estimated_credits` and the remaining balance.
2. Show the user the validated sample plus the estimate and ask before the full run — unless
   the user pre-authorized the spend (a spend cap or a "don't ask about credits" instruction)
   or this is a user-configured autonomous run. In those cases proceed and report credits
   spent in the final summary instead. Asking for the whole table in one prompt is a scope,
   not a spend approval.
3. Start the run with `acknowledged_credits` set to the dry-run's `estimated_credits`. Runs
   estimated above the approval threshold will not start without it.
