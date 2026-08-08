---
name: source-social-audience
description: Source followers, connections, or post engagers from a LinkedIn company page, X account, or LinkedIn post into an Ethos table. Use when a user asks for a competitor's followers, a social audience, page followers, account followers, connections, fans, reactors, or commenters.
catalog_title: Source social audience
catalog_category: Prospecting
catalog_description: Pull a native LinkedIn or X audience into an Ethos people table without browser scraping.
---

# Source Social Audience

Use Ethos's native audience sources. Do not browse, scrape, manually curate, or
approximate an exact follower audience with `find_people`.

1. Call `get_workspace_overview` once when the organization matters. Ask only
   for a missing target URL/account or a user-required limit.
2. Call `list_signal_definitions` and choose the sourceable definition that
   exactly matches the request: company-page followers, account followers,
   first-degree connections, or post reactors/commenters. Use its returned
   `signal_key` and config schema; never invent a key or config field.
3. Branch on the returned definition. For a watch-only definition
   (`sourceable=false`), do not call `pull_signal`: create a draft standing
   workflow with the definition's required trigger config, using
   `trigger_config={}` only when `configuration_mode=managed`. Report the
   returned `urls.workflow`; activate only under the fresh-approval rules in the
   `manage-workflows` skill, and skip `get_signal_pull_status`. For a sourceable
   definition, call `pull_signal` with its required config and `dry_run=true`,
   using `config={}` only when configuration is managed. At or below 100
   estimated credits, repeat with `dry_run=false` without another confirmation.
   Above 100, show the estimate and obtain approval before repeating with
   `dry_run=false` and the estimate as `acknowledged_credits`.
4. For the sourceable branch, call `get_signal_pull_status` with
   `wait_seconds=120`; repeat only if it remains nonterminal. Do not replace this
   with table-read polling.
5. For the sourceable branch, call `inspect_table_summary` for a bounded quality
   sample. Preserve the source table and provenance when enriching or filtering
   it later.
6. For a one-time pull, report target, source type, table ID/URL, delivered rows,
   and failed or skipped counts; a completed zero-row result is not an error.
   For a watch-only definition, report the draft workflow ID and
   `urls.workflow` instead.

For LinkedIn post engagers that should be qualified and turned into outreach,
continue with the `linkedin-post-engagers` skill. For unsupported networks or
audience types, explain that Ethos cannot source them natively; do not silently
broaden the request.
