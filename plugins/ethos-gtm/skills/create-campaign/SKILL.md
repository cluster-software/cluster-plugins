---
name: create-campaign
description: Build, populate, update, or launch an Ethos LinkedIn, email, or mixed-channel campaign through MCP. Use when a user wants to create a campaign end to end, attach or exclude leads, validate or launch a ready draft, update its sequence or settings, or pause or resume outreach.
catalog_title: Create campaign
catalog_category: Campaigns
catalog_description: Create or operate an Ethos campaign - attach lists, add leads, configure sequences, update live outreach, and launch.
---

# Create Campaign

## Build a draft

1. Call `get_workspace_overview` once when the organization, positioning, or
   recent source table is ambiguous, and treat its `active_org` as authoritative.
   If the user explicitly chooses another authorized organization, resolve its
   exact ID with `list_ethos_orgs`, call `switch_ethos_org`, and reload the
   overview before resolving or changing resources. Resolve exact resource IDs
   with `list_tables`, `inspect_table_summary`, and `list_campaigns`; never guess.
2. Resolve the audience:
   - To create a reusable list from a table or CSV, read an attached CSV or
     user-provided local path directly with the client's file capabilities;
     never open a browser upload handoff. If the user names only Desktop or
     Downloads, inspect only that directory and ask which file to use only when
     multiple CSVs are plausible. Ask the user to attach the file or provide an
     accessible exact path only when the client cannot read it. Parse the CSV
     locally into ordered headers and JSON rows, preserving quoted values and
     rejecting empty or malformed input. Call `create_list` with
     `source="csv"` and `dry_run=true` first. Review mapping, invalid, missing,
     existing-contact, and dedupe counts, then repeat the same mapping with
     `dry_run=false`. For more than
     `min(500, floor(100000 / header_count))` rows, first build a people table
     in batches with `create_table` and `append_table_rows`, then call
     `create_list` with `source="table"`.
   - To use an existing list, pass its ID to the campaign or call
     `attach_list_to_campaign` on an existing draft.
   - To stage table rows directly, create the campaign first, then call
     `add_leads_to_campaign` with server-side filters or verified row IDs.
3. Draft concise, channel-correct copy. Use `generate_campaign_copy` and
   `search_copy_bank` only for LinkedIn messages. For email or mixed sequences,
   write the email subject/body directly from the user's brief and workspace
   context; do not relabel LinkedIn output as email. The first email needs a
   subject, and email-only outreach uses `first_step="no_invitation"`.
4. Call `create_campaign_with_sequence`. This creates a draft and can attach a
   list, define the complete sequence, and add at most five AI variables with
   explicit fallbacks. It never launches.
5. After creation, always verify the draft with `get_campaign` and a bounded
   `list_campaign_leads` call, even when the create result is successful. If
   additional audience is needed, stage it with `add_leads_to_campaign` before
   those verification calls.

## Change an existing campaign

- `update_campaign_sequence` replaces the complete future sequence. Include
  every invitation/message step that should remain; already-sent messages are
  unchanged. Immediately call `get_campaign` and confirm the complete future
  sequence matches the requested replacement before reporting success.
- `update_campaign_settings` changes only the supplied campaign settings.
  Immediately call `get_campaign` and confirm every supplied setting matches the
  requested value before reporting success.
- Use `attach_list_to_campaign` or `add_leads_to_campaign` to expand the
  audience, and verify with `get_campaign` plus `list_campaign_leads`.
- Before adding leads to an existing campaign, call `get_campaign`. If it is
  running, explain that the new leads will be enrolled into real outreach and
  obtain explicit approval immediately before `add_leads_to_campaign`.
- To stop selected leads from receiving future outreach, use
  `list_campaign_leads` once to resolve exact `campaign_contact_id` values.
  Explain that queued and scheduled steps will be skipped but an in-flight step
  may still finish, then obtain explicit approval immediately before
  `exclude_campaign_leads`. After that mutation returns, call
  `list_campaign_leads` again to verify the same IDs. Keep this order: read,
  exclude, verify. Report excluded, unchanged, skipped-step, and running-step
  counts.
- For structural changes to running outreach, explain the interruption and get
  explicit approval before `pause_campaign`; update and verify while paused,
  then get explicit approval again before `resume_campaign`.

## Lifecycle safety

`launch_campaign`, `pause_campaign`, `resume_campaign`, and
`exclude_campaign_leads` affect real outreach. Immediately before any one of
them, show the exact campaign, action, and affected campaign-contact IDs and
obtain explicit user approval. After launch, pause, or resume, verify campaign
ID, URL, and status with `get_campaign`. After exclusion, verify affected leads
with `list_campaign_leads` as described above; do not substitute
`get_campaign`. Never treat draft creation as permission to launch.
