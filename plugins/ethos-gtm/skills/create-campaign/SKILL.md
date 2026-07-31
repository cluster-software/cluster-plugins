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
2. **Write the sequence.** Draft 1-3 channel-preserving steps. Ground LinkedIn copy with `generate_campaign_copy` (pass `list_id`, or `campaign_id` for an existing campaign; `direction` to steer; `message_count` for 1-3 steps) or read proven plays with `search_copy_bank`. Review copy with the user before creating the campaign; the sequence can be changed later with `update_campaign_sequence`, but only under the rules below.
3. **Create the campaign.** Call `create_campaign_with_sequence` with `name`, `messages`, `list_id`, and the required sender IDs. Each message accepts `{channel, name?, subject_template?, body_template, wait_amount, wait_unit, media_attachment?}`. Use `channel="EMAIL"` for email steps; the first email requires `subject_template`, while a later email can omit it to reply in the existing thread. Use `first_step="no_invitation"` for email-only sequences. Mixed sequences may use `first_step="invitation"`, and `first_step_name` renames that connection-request step. LinkedIn invitations still pending after `linkedin_invite_withdraw_after_days` days (1-90, default 14) are withdrawn automatically; pass `null` to keep them pending indefinitely, and change it later with `update_campaign_settings`. Pass optional `copy_play` and `ai_variables` from the chosen draft.
   - Template variables like `{{first_name}}` must exist on every imported lead; imports reject below 100% coverage.
   - AI variables (`{key, prompt, fallback}`, max 5) resolve per recipient at enrollment via a research agent (1 credit per contact per variable), need a table-backed lead list, and fall back to the mandatory `fallback` text.
4. **Add leads.** For campaigns with AI variables, call `add_leads_to_campaign` with `source="table"` (`table_id`, `linkedin_column` if not inferred, `standard_field_columns`, `custom_variable_columns`); AI variables cannot resolve from inline contacts. For campaigns without AI variables, use that table source or `source="contacts"` (inline contact objects or `contact_id`s). Drafts import without enrolling; running campaigns enroll immediately. Report imported/enrolled/skipped counts and `variable_coverage`.
5. **Launch.** `launch_campaign` is destructive: it enrolls the list and starts real sends on every configured channel. Confirm explicitly with the user before calling. If it reports a missing LinkedIn or Gmail account, send the user to the campaign URL to pick that sender, then call `launch_campaign` again.
6. **Verify and hand off.** Call `get_campaign` to confirm status, sequence steps, and contact counts, then return the campaign ID and campaign URL. Use `list_campaigns` to find existing campaign IDs when the user references a campaign by name.

## Updating an existing sequence

`update_campaign_sequence` replaces the campaign's **future** outreach. It is a full replacement, not a patch: every message you omit is removed, and settings you do not resend fall back to defaults.

1. **Read the current sequence first.** Call `get_campaign` and copy `data.sequence_update_input`. It is a ready-made request body - `first_step`, `first_step_name`, `invitation_note_template`, and every message with its `wait_amount`/`wait_unit`, `subject_template`, and `media_attachment`. Edit that object and send it back. Do not hand-build the payload from `data.sequence`; the wait values there belong to the preceding step and you will shift the campaign's timing.
2. **Check what the campaign's status allows.**
   - `draft` / `recommended`: anything.
   - `running`: copy, subject, timing, invitation note, and attachments on the steps that already exist. Adding or removing a step is rejected.
   - `paused`: also add and remove message steps.
   - `completed` / `archived`: rejected.
3. **Pause before a structural change.** Call `pause_campaign` to stop new sends, make the change, verify it, then `resume_campaign`. Both are destructive - confirm each with the user, and tell them the campaign is not sending while paused.
4. **Send the update.** Call `update_campaign_sequence` with `campaign_id`, an explicit `first_step`, and the complete `messages` array in send order. The same email-subject and invitation-note rules as campaign creation apply. Only three fields survive being omitted - `first_step_name`, and a message's `name` and `media_attachment` when it lines up with an existing same-channel step. Everything else, including `invitation_note_template`, `subject_template`, `wait_amount`, and `wait_unit`, is cleared or reset to its default when you leave it out. Send `null` explicitly to clear an attachment or a name on purpose. This is why step 1 starts from `sequence_update_input`.
5. **Verify.** Call `get_campaign` again and read back the saved steps to the user before resuming.

What the update does to leads already in the campaign:

- Already-sent messages are never resent or rewritten.
- Contacts still waiting on a step get the new copy for the steps ahead of them.
- Pending sends on a removed step are skipped, and contacts sitting on that step are marked completed.
- Contacts who already finished the sequence are **not** backfilled into newly added steps.

## Limits

- LinkedIn, email, and mixed outreach campaigns are supported; gifting campaigns cannot be created over MCP.
- After launch, a step's channel cannot change, and the invitation first step cannot be added or removed - though its name and note stay editable. To change either, build a new campaign.
- A step that is mid-send blocks removal; retry once it finishes.
- No MCP tool yet to change the sender. Send the user to the campaign page for that.
