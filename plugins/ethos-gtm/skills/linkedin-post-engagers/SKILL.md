---
name: linkedin-post-engagers
description: Turn people who reacted to or commented on a LinkedIn post into a qualified, personalized Ethos campaign using the active customer's saved ICP and workspace context. Use when a user provides a LinkedIn post URL or an existing post-engagers table and wants to qualify engagers, generate customer-specific outreach, or create a draft campaign.
catalog_title: LinkedIn post engagers
catalog_category: Campaigns
catalog_description: Qualify LinkedIn post engagers against the customer's saved ICP, generate personalized outreach, and create a reviewed draft campaign.
---

# LinkedIn Post Engagers

Load the current server-authored workflow before acting:

1. Read `skill://ethos/linkedin-post-engagers/SKILL.md` when this client exposes
   MCP resources.
2. Otherwise call `load_ethos_skill` with `name="linkedin-post-engagers"` and
   `header_only=false`.
3. Follow the returned workflow in full, including its customer-data and launch
   safety requirements.

This file is only an intent router. If neither loading path is available, ask
the user to update or reconnect Ethos instead of improvising a workflow.
