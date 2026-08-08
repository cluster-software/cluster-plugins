---
name: enrich-contact-info
description: Enrich work emails and phone numbers in an Ethos people table using MCP.
catalog_title: Enrich contact info
catalog_category: Enrichment
catalog_description: Find work emails and phone numbers for selected people-table rows.
---

# Enrich Contact Info

1. Call `inspect_table_summary` and confirm the target is a people table. A
   company table must first be materialized with `create_people_table` after its
   people-sourcing run finishes.
2. Call `enrich_contact_info` with `scope="first_5"`; request only the fields the
   user needs, normally `work_email` before `phone`. Supply `input_column_id`
   only when Ethos cannot infer the profile column.
3. Wait with `get_column_run_status` using `wait_seconds=120`; never poll by
   repeatedly reading the table. Inspect the sample with
   `inspect_table_summary`.
4. Before a broader run, call `enrich_contact_info` with the returned
   `column_id`, intended scope, and `dry_run=true`. At or below 100 estimated
   credits, proceed without another confirmation. Above 100, show the estimate
   and obtain approval, then repeat with that estimate as
   `acknowledged_credits`.
5. Use `scope="empty"` to fill remaining rows and `force_refresh` only when the
   user explicitly needs to bypass cached contact data. Wait on the new run and
   report requested fields, selected rows, credits, terminal status, and
   failures.
