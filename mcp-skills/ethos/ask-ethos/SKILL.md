---
name: ask-ethos
description: Read-only analysis of Ethos campaign progress, status, performance, replies, and lead cohorts through MCP. Use when a user asks how campaigns are doing, wants campaigns compared, wants reply themes or quality reviewed, asks why a campaign is stalled or underperforming, or wants to know which lead segments have higher or lower reply rates.
catalog_title: Ask Ethos
catalog_category: Campaigns
catalog_description: Compare campaign performance, inspect replies, and find lead-segment patterns without changing campaigns or sending messages.
---

# Ask Ethos

Use only the read-only Ethos intent tools. Never create, update, launch, pause,
resume, enrich, or send while following this skill.

1. Call `get_workspace_overview` once when the active organization or saved GTM
   context matters. Switch only when the user explicitly chooses another org.
2. Call `analyze_campaigns` with campaign names/IDs or a status filter. Continue
   with its cursor when needed; do not compare drafts as if they had launched.
3. Compare like-for-like denominators: replies per contacted lead, acceptance per
   invitation, and channel-specific reply rates. Treat small cohorts as
   directional, separate observations from hypotheses, and do not invent missing
   cohorts or evidence.
4. When reply content is relevant, call `search_conversations`, then
   `get_conversation` only for the bounded conversations needed. Never call
   `send_reply` from this skill.

Lead with the answer, then state scope, data freshness, material evidence,
confidence limits, and the most useful read-only follow-up.
