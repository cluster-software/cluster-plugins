---
name: enrich-contact-info
description: Enrich work emails and phone numbers in an Ethos people table using MCP.
catalog_title: Enrich contact info
catalog_category: Enrichment
catalog_description: Find work emails and phone numbers for selected people-table rows.
---

# Enrich Contact Info

1. Call `inspect_table` and confirm the target is a people table. If sourcing
   began from a company table, use the people table returned by `find_people` or
   `get_job_status`.
2. Generate one idempotency key and call `enrich_contact_info` on a small
   selection, normally requesting `work_email` first. Supply the profile input
   column only when Ethos cannot infer it.
3. If the result is `input_required`, surface the quote and retry with its
   `quote_id` after approval. Do not ask again at or below 100 credits.
4. For `working`, call `get_job_status` with `wait_seconds=120`; never poll by
   repeatedly reading the table.
5. Inspect the sample, then reuse the returned contact-info column for the
   broader row/filter selection. Use `force_refresh` only when the user needs to
   bypass cached contact data.

Report requested fields, selected rows, terminal status, credits, and failures.
