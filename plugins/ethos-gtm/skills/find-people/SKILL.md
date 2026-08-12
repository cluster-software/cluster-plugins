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
   - CSV or another readable local file: read the attachment or user-provided
     path with the client's file capabilities. When the user names only a
     directory such as Desktop or Downloads, inspect only that directory and
     use the single plausible CSV; ask one concise disambiguation question when
     multiple files are plausible. Never open a browser upload handoff. If the
     file is not readable from the current client, ask the user to attach it or
     provide an accessible exact path.

     Parse the file locally into ordered headers and JSON rows. Preserve quoted
     values and header order, discard fully blank rows, and stop on an empty or
     malformed CSV or blank/duplicate headers. Classify rows with person-level
     identity (for example, a person's LinkedIn URL or a name plus title/email)
     as people; classify company/domain rows without person identity as
     companies. Ask which shape the user intended only when the columns are
     genuinely ambiguous.

     For a table import, send at most
     `min(500, floor(100000 / header_count))` rows per call. Create the first
     batch with `create_table`, preserving the file name in `source_filename`,
     and send later batches with `append_table_rows` as
     `{"rows":[{"values": row}, ...]}`. Use `entity_type="company"` for a
     company CSV, then continue through the existing-company-table path below.
     Use `entity_type="people"` for a people CSV and inspect the completed
     table directly.

     When the user explicitly wants a reusable campaign/contact list and the
     people CSV has the person identity columns supported by `create_list`
     (currently a mapped LinkedIn profile column for table/CSV imports), call
     `create_list` with `source="csv"` and `dry_run=true`, review its mapping and
     dedupe counts, then repeat the same request with `dry_run=false`. For an
     input larger than one table batch, first build the people table in batches
     and use `create_list` with `source="table"` instead.
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
3. Inspect a returned people table with `inspect_table_summary` for a bounded
   quality sample. Do not enumerate a whole table merely to select rows for the
   next operation; downstream tools accept filters or row IDs. For a direct
   list import, use the `create_list` preview and final counts instead.
4. Report the resulting table or list IDs/URLs, matched or imported people,
   skipped/failed counts, and any refinement suggestion. A successful
   zero-match result is not an error.
