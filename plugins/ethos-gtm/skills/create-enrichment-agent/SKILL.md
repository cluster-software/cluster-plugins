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

`run_table_column` spends org credits per billable row. Validate the sample before a full run,
then use the server's approval decision instead of asking about every paid action:

1. Call `run_table_column` with `dry_run: true` and the intended full scope to get
   `estimated_credits`, the remaining balance, `approval_threshold_credits`, and
   `approval_required`.
2. When `approval_required` is false (currently estimates at or below 100 credits), start the
   run immediately with `dry_run: false`. Do not ask the user for confirmation; report the
   credits spent in the final summary.
3. When `approval_required` is true (currently estimates above 100 credits), show the user the
   validated sample plus the estimate and ask before the full run — unless the user
   pre-authorized the spend (a spend cap or a "don't ask about credits" instruction) or this
   is a user-configured autonomous run. Asking for the whole table in one prompt is a scope,
   not a spend approval.
4. After approval or pre-authorization, start the run with `acknowledged_credits` set to the
   dry-run's `estimated_credits`.
