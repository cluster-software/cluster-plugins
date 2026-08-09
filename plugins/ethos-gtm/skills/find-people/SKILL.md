---
name: find-people
description: Find prospects from a natural-language ICP using Ethos MCP.
catalog_title: Find people
catalog_category: Prospecting
catalog_description: Turn a natural-language ICP, search URL, CSV, or company table into a people table.
---

# Find People

1. Call `get_workspace_overview` once when the active organization or saved ICP
   matters. Ask one consolidated question only when the request lacks a usable
   company ICP or target-person description.
2. Choose exactly one source path:
   - Natural-language ICP: call `find_people` with `dry_run=true`, describing
     both target companies and people. Make exactly one dry-run call unless it
     returns `needs_refinement`. At or below 100 estimated credits, immediately
     repeat the same validated request with `dry_run=false`; do not rewrite the
     query or request another estimate. Above 100, show the estimate and obtain
     approval before passing it as `acknowledged_credits`. After the real call
     returns a `search_id`, always wait with `get_find_people_status` and
     `wait_seconds=120`. If either call returns `needs_refinement`, refine the
     query instead of pretending a search started.
   - LinkedIn or Sales Navigator people-search URL: call
     `create_salesnav_import` with `dry_run=true`; follow the same 100-credit
     approval boundary, then start it and call `get_salesnav_import_status`
     with `wait_seconds=120`.
   - CSV: call `create_csv_upload_handoff`, give the secure handoff to the user,
     then wait with `get_upload_handoff_status` after upload.
   - Existing company table: inspect it with `inspect_table_summary`. Call
     `source_people_from_company_table` with the required server-side filters,
     source input columns, a targeting brief grounded in the requested people,
     `scope="first_5"`, and `dry_run=false`. Wait with
     `get_column_run_status` and inspect quality. Reuse the returned `column_id`
     with `run_table_column` for the remaining matching companies: first call it
     with `scope="empty"` and `dry_run=true`, then repeat with
     `scope="empty"` and `dry_run=false` automatically at or below 100 credits,
     or obtain approval above 100 before also passing `acknowledged_credits`.
     Wait on that run with `get_column_run_status`. Once terminal, call
     `create_people_table` with the same source column and `source_column_ids`
     for every source field needed as signal, qualification, or campaign context.
3. Inspect the returned people table with `inspect_table_summary` for a bounded
   quality sample. Do not enumerate a whole table merely to select rows for the
   next operation; downstream tools accept filters or row IDs.
4. Report company and people table IDs/URLs, matched people, skipped/failed
   counts, and any refinement suggestion. A successful zero-match result is not
   an error.
