---
name: enrich-contact-info
description: Enrich work emails and phone numbers in an Ethos people table using MCP.
---

# Enrich Contact Info

Use Ethos MCP first.

1. Identify the people table and the LinkedIn/profile input column if needed.
2. Call `enrich_contact_info_sample` with requested fields, usually `["work_email"]` first.
3. Inspect or open the table for sample quality.
4. Call `enrich_remaining_contact_info` with the returned contact-info `column_id` when the sample looks right.

Return run IDs, table URL, total rows, and the next action. Avoid broad enrichment until a sample run is accepted.
