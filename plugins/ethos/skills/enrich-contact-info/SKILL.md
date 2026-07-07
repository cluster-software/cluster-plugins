---
name: enrich-contact-info
description: Enrich work emails and phone numbers in an Ethos people table using MCP.
---

# Enrich Contact Info

Use Ethos MCP first.

1. Identify the people table and the LinkedIn/profile input column if needed. The `table_id` must be a PEOPLE table, never the company table a sourcing run started from: `inspect_table_summary` on the company table returns the linked `people_table_id` once it exists, and `create_people_table` materializes it from a finished sourcing run when it does not.
2. Call `enrich_contact_info` with `scope: "first_5"` and requested fields, usually `["work_email"]` first.
3. Inspect or open the table for sample quality.
4. Call `enrich_contact_info` with the returned contact-info `column_id` and `scope: "empty"` when the sample looks right.

Return run IDs, table URL, total rows, and the next action. Avoid broad enrichment until a sample run is accepted.
