---
name: enrich-contact-info
description: Enrich work emails and phone numbers in an Ethos people table using MCP.
catalog_title: Enrich contact info
catalog_category: Enrichment
catalog_description: Add work emails and optional phone numbers to a people table using Ethos contact data enrichment and org-level credit checks.
---

# Enrich Contact Info

Use Ethos MCP first.

1. Identify the people table and the LinkedIn/profile input column if needed. The `table_id` must be a PEOPLE table, never the company table a sourcing run started from: `inspect_table_summary` on the company table returns the linked `people_table_id` once it exists, and `create_people_table` materializes it from a finished sourcing run when it does not.
2. Call `enrich_contact_info` with `scope: "first_5"` and requested fields, usually `["work_email"]` first. Wait for the returned `run_id` with `get_column_run_status` and `wait_seconds=120`; call status again only if it remains nonterminal, never by re-reading the table in a loop.
3. Inspect or open the table for sample quality.
4. Call `enrich_contact_info` with the returned contact-info `column_id` and `scope: "empty"` when the sample looks right. For a specific displayed batch, pass both `lower_range` and `upper_range` as 1-based inclusive bounds. Wait for completion with the same blocking `get_column_run_status` pattern.

Return run IDs, table URL, total rows, and the next action. Avoid broad enrichment until a sample run is accepted.

## Credit approval

`enrich_contact_info` spends org credits per billable row; rows with a fresh cached result
are free. Validate the sample before a full run, then use the server's approval decision
instead of asking about every paid action:

1. Call `enrich_contact_info` with `dry_run: true` and the intended full scope. The response
   returns `estimated_credits`, billable/cached row counts, the remaining balance,
   `approval_threshold_credits`, and `approval_required`.
2. When `approval_required` is false (currently estimates at or below 100 credits), start the
   run immediately with `dry_run: false`. Do not ask the user for confirmation; report the
   credits spent in the final summary.
3. When `approval_required` is true (currently estimates above 100 credits), show the user the
   sample rows plus the estimate and ask before starting — unless the user pre-authorized the
   spend (a spend cap or a "don't ask about credits" instruction) or this is a user-configured
   autonomous run. Asking for the whole table in one prompt is a scope, not a spend approval.
4. After approval or pre-authorization, start the run with `acknowledged_credits` set to the
   dry-run's `estimated_credits`.
