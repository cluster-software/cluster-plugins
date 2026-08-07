---
name: ask-ethos
description: Read-only analysis of Ethos campaign progress, status, performance, replies, and lead cohorts through MCP. Use when a user asks how campaigns are doing, wants campaigns compared, wants reply themes or quality reviewed, asks why a campaign is stalled or underperforming, or wants to know which lead segments have higher or lower reply rates.
catalog_title: Ask Ethos
catalog_category: Campaigns
catalog_description: Compare campaign performance, inspect replies, and find lead-segment patterns without changing campaigns or sending messages.
---

# Ask Ethos

Load the current server-authored workflow before acting:

1. Read `skill://ethos/ask-ethos/SKILL.md` when this client exposes MCP resources.
2. Otherwise call `load_ethos_skill` with `name="ask-ethos"` and
   `header_only=false`.
3. Follow the returned workflow in full.

This file is only an intent router. If neither loading path is available, ask
the user to update or reconnect Ethos instead of improvising a workflow.
