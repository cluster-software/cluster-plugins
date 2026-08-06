---
name: create-campaign
description: Build, populate, update, or launch an Ethos LinkedIn, email, or mixed-channel campaign through MCP. Use when a user wants to create a campaign end to end, attach a list, add leads to an existing campaign, validate or launch a ready draft, update its sequence or settings, or pause or resume outreach.
catalog_title: Create campaign
catalog_category: Campaigns
catalog_description: Create or operate an Ethos campaign - attach lists, add leads, configure sequences, update live outreach, and launch.
---

# Create Campaign

Use the direct intent tools; never search for or dispatch another tool.

## Build a draft

1. Call `get_workspace_overview` once when org or positioning is ambiguous.
2. Resolve the people table/list and draft a concise channel-preserving sequence.
   Email's first message needs a subject. Use `first_step="no_invitation"` for
   email-only outreach.
3. Generate one idempotency key and call `build_campaign_draft`. It can create a
   list from `leads`, map custom variables, create the sequence/settings, define
   campaign AI variables, and stage leads. It never launches.
4. Call `analyze_campaigns` for the returned campaign to verify status,
   configuration, and staged count.

## Change an existing campaign

- Call `update_campaign` with exactly one change: `add_leads`,
  `replace_sequence`, or `update_settings`. A sequence replacement is complete,
  so include every future step that should remain.
- For structural changes to live outreach, pause first, update, verify, then
  resume. Already-sent messages are never rewritten.
- Reuse the same idempotency key only for an exact retry. Use a new key for a
  new intentional change.

## Lifecycle safety

`set_campaign_state` is destructive. Immediately before `launch`, `pause`, or
`resume`, show the exact campaign and action and obtain explicit user approval.
Launch starts real sends. After the call, verify with `analyze_campaigns` and
report the campaign ID, URL, status, and affected lead count.
