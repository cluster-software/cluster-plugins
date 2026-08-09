---
name: ask-ethos
description: Read-only analysis of Ethos campaign progress, status, performance, replies, and lead cohorts through MCP. Use when a user asks how campaigns are doing, wants campaigns compared, wants reply themes or quality reviewed, asks why a campaign is stalled or underperforming, or wants to know which lead segments have higher or lower reply rates.
catalog_title: Ask Ethos
catalog_category: Campaigns
catalog_description: Compare campaign performance, inspect replies, and find lead-segment patterns without changing campaigns or sending messages.
---

# Ask Ethos

Use only read-only Ethos tools. Never create, update, enrich, launch, pause,
resume, archive, or send a message while following this skill.

1. Call `get_workspace_overview` once when the active organization or saved GTM
   context matters, and treat its `active_org` as authoritative. If the user
   explicitly chooses another authorized organization, resolve its exact ID with
   `list_ethos_orgs`, call `switch_ethos_org`, then reload the overview before
   resolving resources. Never switch organizations implicitly.
2. Use `list_campaigns` to resolve campaign IDs. For each relevant campaign,
   call `get_campaign`, `get_campaign_performance`, and a bounded
   `list_campaign_leads` cohort. Continue with offsets only when the question
   requires more leads. For identity or cross-campaign membership questions,
   use `list_campaign_leads` with exact campaign IDs, statuses, or one exact
   LinkedIn URL, email, or full name; do not reconstruct memberships from
   source tables or inbox conversations.
3. Compare like-for-like denominators: replies per contacted lead, acceptance
   per invitation, and channel-specific reply rates. Do not treat drafts as
   launched campaigns or turn small samples into confident conclusions.
4. When reply content matters, call `list_unibox_conversations` in its default
   campaign-conversation scope, then `get_unibox_conversation` only for the
   bounded conversations needed. Set `include_all=true` only when the user
   explicitly requests organic account conversations. Never call
   `send_unibox_message` from this skill.
5. Separate observed facts from hypotheses. Lead with the answer, then state
   scope, freshness, material evidence, confidence limits, and the most useful
   read-only follow-up.
