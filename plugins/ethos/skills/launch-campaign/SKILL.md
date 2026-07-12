---
name: launch-campaign
description: Add leads to an existing Ethos campaign, attach lists, or launch a ready draft through MCP.
---

# Launch Campaign

Use Ethos MCP first. To build a campaign from scratch (sequence, leads, launch), use the `create-campaign` skill.

1. If the user already has a campaign, call `add_leads_to_campaign` with a table source or contact IDs. Find the campaign ID with `list_campaigns` (via `call_ethos_tool`) when the user references it by name. Drafts import without enrolling; running campaigns enroll immediately.
2. If a list or campaign must be created or configured, call `search_ethos_tools` (query "campaign") and use `call_ethos_tool` for `create_list`, `attach_list_to_campaign`, `create_campaign_with_sequence`, or related operations.
3. To launch a ready draft, call `launch_campaign` - destructive: it starts real sends on every campaign channel, so confirm with the user first. The campaign must have a lead list plus a connected LinkedIn sender for LinkedIn steps and a connected Gmail sender for email steps (set at creation or on the campaign page).

Keep campaign writes explicit. Return campaign ID, lead import ID, counts, and campaign URL.
