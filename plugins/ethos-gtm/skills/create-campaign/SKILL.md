---
name: create-campaign
description: Build, populate, update, or launch an Ethos LinkedIn, email, or mixed-channel campaign through MCP. Use when a user wants to create a campaign end to end, attach a list, add leads to an existing campaign, validate or launch a ready draft, update its sequence or settings, or pause or resume outreach.
catalog_title: Create campaign
catalog_category: Campaigns
catalog_description: Create or operate an Ethos campaign - attach lists, add leads, configure sequences, update live outreach, and launch.
---

# Create Campaign

Load the current server-authored workflow before acting:

1. Read `skill://ethos/create-campaign/SKILL.md` when this client exposes MCP
   resources.
2. Otherwise call `load_ethos_skill` with `name="create-campaign"` and
   `header_only=false`.
3. Follow the returned workflow in full, including every approval and
   idempotency requirement.

This file is only an intent router. If neither loading path is available, ask
the user to update or reconnect Ethos instead of improvising a workflow.
