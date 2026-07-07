---
name: create-campaign
description: Build and launch an Ethos LinkedIn campaign end to end through MCP - lead list, message sequence, AI personalization variables, leads, and launch - without the UI. Use when the user wants a campaign created, written, or launched.
---

# Create Campaign

Use Ethos MCP. Campaign tools are searchable: load them with `search_ethos_tools` (query "campaign") and invoke them with `call_ethos_tool`. Only `add_leads_to_campaign` is a default tool.

## Preconditions

1. Confirm the org with `get_current_ethos_org`; call `switch_ethos_org` first if the user means another authorized org.
2. Know the lead source: an Ethos people table (from `find_people` or a CSV upload handoff) or explicit contacts.
3. Ask which connected LinkedIn sender account to use. Launch requires `connected_account_id` on the campaign, MCP cannot list connected accounts, and MCP can only set it at creation. If the user does not know the ID, create the campaign without it and have them pick the sender on the campaign page before launch.

## Workflow

1. **Create the lead list.** Call `create_list` with a campaign-specific name. The campaign needs a `list_id` before `add_leads_to_campaign` will accept leads.
2. **Write the sequence.** Draft 1-3 messages. Ground them with `generate_campaign_copy` (pass `list_id`, or `campaign_id` for an existing campaign; `direction` to steer; `message_count` for 1-3 steps) or read proven plays with `search_copy_bank`. Review copy with the user before creating the campaign - sequences cannot be edited over MCP after creation.
3. **Create the campaign.** Call `create_campaign_with_sequence` with `name`, `messages` (each `{name?, body_template, wait_amount, wait_unit}`), `list_id`, `connected_account_id`, and `first_step` (`invitation` opens with a connection request), plus optional `copy_play` and `ai_variables` from the chosen draft.
   - Template variables like `{{first_name}}` must exist on every imported lead; imports reject below 100% coverage.
   - AI variables (`{key, prompt, fallback}`, max 5) resolve per recipient at enrollment via a research agent (1 credit per contact per variable), need a table-backed lead list, and fall back to the mandatory `fallback` text.
4. **Add leads.** Call `add_leads_to_campaign` with `source="table"` (`table_id`, `linkedin_column` if not inferred, `standard_field_columns`, `custom_variable_columns`) or `source="contacts"` (inline contact objects or `contact_id`s). Drafts import without enrolling; running campaigns enroll immediately. Report imported/enrolled/skipped counts and `variable_coverage`.
5. **Launch.** `launch_campaign` is destructive: it enrolls the list and starts real LinkedIn sends. Confirm explicitly with the user before calling. If it fails with "requires a connected LinkedIn account", send the user to the campaign URL to pick the sender, then call `launch_campaign` again.
6. **Hand off.** Return the campaign ID and campaign URL. There is no MCP read-back for campaign status; monitoring, pausing, and sequence edits happen on the campaign page.

## Limits

- LinkedIn campaigns only; gifting campaigns cannot be created over MCP.
- No MCP tools yet to read/list campaigns, edit a sequence, change the sender, or pause/resume. To change a draft's sequence, create a new draft campaign and re-add leads, or edit it in the UI.
