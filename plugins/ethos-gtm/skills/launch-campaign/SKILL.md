---
name: launch-campaign
description: Add leads to an existing Ethos campaign, attach lists, or launch a ready draft through MCP.
catalog_title: Launch campaign
catalog_category: Campaigns
catalog_description: Add leads to an existing Ethos campaign, attach lists, or launch a ready draft.
---

# Launch Campaign

Use Ethos MCP first. To build a campaign from scratch (sequence, leads, launch), use the `create-campaign` skill.

1. If the user already has a campaign, call `add_leads_to_campaign` with a table source or contact IDs. Find the campaign ID with `list_campaigns` (via `call_ethos_tool`) when the user references it by name. Drafts import without enrolling; running campaigns enroll immediately.
2. If a list or campaign must be created or configured, call `search_ethos_tools` (query "campaign") and use `call_ethos_tool` for `create_list`, `attach_list_to_campaign`, `create_campaign_with_sequence`, or related operations.
3. To launch a ready draft, call `launch_campaign` - destructive: it starts real sends on every campaign channel, so confirm with the user first. The campaign must have a lead list plus a connected LinkedIn sender for LinkedIn steps and a connected Gmail sender for email steps (set at creation or on the campaign page).
4. To stop or restart sends on a live campaign, call `pause_campaign` or `resume_campaign` - destructive: confirm explicitly with the user before either call. Each requires the matching status - only a `running` campaign pauses, only a `paused` one resumes. Pausing is also the precondition for adding or removing sequence steps; the `create-campaign` skill covers that workflow.

Keep campaign writes explicit. Return campaign ID, lead import ID, counts, and campaign URL.
