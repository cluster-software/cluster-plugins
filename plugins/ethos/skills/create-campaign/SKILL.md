---
name: create-campaign
description: Build and launch an Ethos LinkedIn, email, or mixed-channel campaign end to end through MCP - lead list, sequence, AI personalization variables, leads, and launch - without the UI.
catalog_title: Create campaign
catalog_category: Campaigns
catalog_description: Build an Ethos LinkedIn, email, or mixed-channel campaign end to end - lead list, sequence, and AI personalization variables.
---

# Create Campaign

Use Ethos MCP. Campaign tools are searchable: load them with `search_ethos_tools` (query "campaign") and invoke them with `call_ethos_tool`. Only `add_leads_to_campaign` is a default tool.

## Preconditions

1. Confirm the org with `get_current_ethos_org`; call `switch_ethos_org` first if the user means another authorized org.
2. Know the lead source: an Ethos people table (from `find_people` or a CSV upload handoff) or explicit contacts.
3. Resolve the sender accounts required by the sequence. LinkedIn steps require `connected_account_id`; email steps require `email_connected_account_id`. Call `list_campaigns` and reuse the appropriate account IDs from a past campaign, or ask the user. If an ID cannot be resolved, create the draft without it and have the user pick the sender on the campaign page before launch.

## Workflow

1. **Create the lead list.** Call `create_list` with a campaign-specific name. The campaign needs a `list_id` before `add_leads_to_campaign` will accept leads.
2. **Write the sequence.** Draft 1-3 channel-preserving steps. Ground LinkedIn copy with `generate_campaign_copy` (pass `list_id`, or `campaign_id` for an existing campaign; `direction` to steer; `message_count` for 1-3 steps) or read proven plays with `search_copy_bank`. Review copy with the user before creating the campaign - sequences cannot be edited over MCP after creation.
3. **Create the campaign.** Call `create_campaign_with_sequence` with `name`, `messages`, `list_id`, and the required sender IDs. Each message accepts `{channel, name?, subject_template?, body_template, wait_amount, wait_unit}`. Use `channel="EMAIL"` for email steps; the first email requires `subject_template`, while a later email can omit it to reply in the existing thread. Use `first_step="no_invitation"` for email-only sequences. Mixed sequences may use `first_step="invitation"`. Pass optional `copy_play` and `ai_variables` from the chosen draft.
   - Template variables like `{{first_name}}` must exist on every imported lead; imports reject below 100% coverage.
   - AI variables (`{key, prompt, fallback}`, max 5) resolve per recipient at enrollment via a research agent (1 credit per contact per variable), need a table-backed lead list, and fall back to the mandatory `fallback` text.
4. **Add leads.** Call `add_leads_to_campaign` with `source="table"` (`table_id`, `linkedin_column` if not inferred, `standard_field_columns`, `custom_variable_columns`) or `source="contacts"` (inline contact objects or `contact_id`s). Drafts import without enrolling; running campaigns enroll immediately. Report imported/enrolled/skipped counts and `variable_coverage`.
5. **Launch.** `launch_campaign` is destructive: it enrolls the list and starts real sends on every configured channel. Confirm explicitly with the user before calling. If it reports a missing LinkedIn or Gmail account, send the user to the campaign URL to pick that sender, then call `launch_campaign` again.
6. **Verify and hand off.** Call `get_campaign` to confirm status, sequence steps, and contact counts, then return the campaign ID and campaign URL. Use `list_campaigns` to find existing campaign IDs when the user references a campaign by name.

## Limits

- LinkedIn, email, and mixed outreach campaigns are supported; gifting campaigns cannot be created over MCP.
- No MCP tools yet to edit a sequence, change the sender, or pause/resume. To change a draft's sequence, create a new draft campaign and re-add leads, or edit it in the UI.
