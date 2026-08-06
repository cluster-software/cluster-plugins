---
name: find-people
description: Find prospects from a natural-language ICP using Ethos MCP.
catalog_title: Find people
catalog_category: Prospecting
catalog_description: Turn a natural-language ICP, search URL, CSV, or company table into a people table.
---

# Find People

1. Call `get_workspace_overview` once when the org or saved ICP matters.
2. Generate one idempotency key and choose exactly one `find_people` request:
   - `brief`: natural-language ICP;
   - `search_url`: a supported saved-search URL;
   - `csv_handoff`: secure user upload;
   - `company_table`: source relevant roles at selected companies.
3. For `input_required`, handle the returned action:
   - open the secure CSV handoff and wait on its job; or
   - show a >100-credit quote and retry with `quote_id` after approval.
4. For `working`, call `get_job_status` with the returned job and
   `wait_seconds=120`. Repeat only if it remains nonterminal.
5. Call `inspect_table` on the returned people table for a bounded quality
   sample. Do not paginate the entire table merely to select rows for the next
   operation; pass filters or row IDs server-side.

Report the table IDs/URLs, matched people, credits, skipped/failed counts, and
any refinement suggestion. A successful zero-match result is not an error.
