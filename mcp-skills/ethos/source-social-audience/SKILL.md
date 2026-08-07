---
name: source-social-audience
description: Source followers, connections, or post engagers from a LinkedIn company page, X account, or LinkedIn post into an Ethos table. Use when a user asks for a competitor's followers, a social audience, page followers, account followers, connections, fans, reactors, or commenters.
catalog_title: Source social audience
catalog_category: Prospecting
catalog_description: Pull a native LinkedIn or X audience into an Ethos people table without browser scraping.
---

# Source Social Audience

Use Ethos's native audience sources. Do not browse, scrape, or manually curate
identities when one of these sources applies, and do not reconstruct an exact
follower audience with `find_people`.

1. Call `get_workspace_overview` once when the organization or saved GTM
   context matters. Ask only for a missing target URL/account; use the schema's
   default limit unless the user specified another one.
2. Generate one idempotency key and call `source_signal` with exactly one typed
   request:
   - LinkedIn company-page followers: `signal_key="linkedin_page_followers"`;
     config requires `company_url` and accepts `max_followers` from 100 to 1000.
   - X account followers: `signal_key="x_account_followers"`; config requires
     `account` and accepts `max_followers` from 200 to 10000 in multiples of 200.
   - LinkedIn post reactors/commenters: `signal_key="post_engagers"`; config
     requires `post_url` and accepts inclusion flags plus bounded reaction and
     comment limits.
   - First-degree LinkedIn connections for connected workspace accounts:
     `signal_key="linkedin_connections"`; config can select connected account
     IDs and a recent-connection window.
   Pass the selected `signal_key` and `config` directly to the tool. Never
   invent another signal key.
3. For `input_required`, display the returned quote and retry only after
   approval, preserving the request and idempotency key and adding `quote_id`.
   For `working`, call `get_job_status` with `wait_seconds=120`; repeat only
   while the job remains nonterminal.
4. Call `inspect_table` for a bounded quality sample. Preserve the source table
   and its provenance when enriching or filtering it later.
5. Report the target, source type, table ID/URL, delivered rows, any approved
   quote, and failed or skipped counts. A completed zero-row result is not an
   error.

If the user wants to qualify LinkedIn post engagers and build outreach, load
and follow `linkedin-post-engagers` after sourcing. For any unsupported social
network or audience type, explain that Ethos cannot source it natively; do not
silently switch to browser collection or broaden the request to approximate
people.
