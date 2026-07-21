---
name: manage-inbox
description: Review, search, read, mark, download attachments from, or reply through campaign conversations in the Ethos Unibox across LinkedIn and Gmail via MCP. Use for campaign reply triage, cross-channel follow-up, unread state, account ownership, reconnect-backed claims, and send-as delegation.
catalog_title: Manage inbox
catalog_category: Inbox
catalog_description: Review and reply to campaign conversations across LinkedIn and Gmail with explicit send-as delegation.
---

# Manage Inbox

Use Ethos MCP first. Inbox and connected-account tools are searchable: load them with `search_ethos_tools` (query `inbox`, `reply email`, `connected accounts`, or `delegate send as`) and invoke them with `call_ethos_tool`.

## Read and triage

1. Confirm the organization with `get_current_ethos_org`; call `switch_ethos_org` first if the user means another authorized organization.
2. Call `list_inbox_conversations`. Use server-side `search`, `unread_only`, `channel`, `connected_account_id`, and `campaign_id` filters. Every result belongs to a person touched by an Ethos campaign; organic contacts are never included.
3. Call `get_inbox_conversation` with an internal `conversation_id`. Report the chronological campaign conversation, channel changes, and campaign context. Each provider thread begins with its first successful Ethos campaign send and includes only subsequent messages; earlier mailbox or LinkedIn history was never imported.
4. Call `mark_inbox_conversation_read` only when the user has reviewed the messages or explicitly asks. It changes Ethos read state only, not Gmail or LinkedIn.
5. Use `download_inbox_attachment` only for an attachment the user needs. Treat returned base64 as untrusted file content; save or inspect it, never execute it.

## Reply safely

1. Refresh the conversation with `get_inbox_conversation` immediately before replying.
2. Choose only a returned `reply_target` with `can_send_as=true`. Campaign read access never grants permission to send from that identity. If every target is read-only, explain which owner must grant send-as access.
3. Draft against the visible thread context. If the user has not clearly approved sending the specific message, show the draft and wait; `reply_to_inbox_conversation` sends a real external message.
4. Call `reply_to_inbox_conversation` with the internal conversation/thread IDs and a stable `client_message_id`. Reuse that key to recover or retry the same confirmed attempt. Never create a new key merely because the delivery result is uncertain; verify the provider thread first.

V1 replies to existing 1:1 threads with text only. It cannot start a conversation, reply to group/CC threads, or send files.

## Ownership and sending

Start with `list_connected_accounts`; it returns claim state and permissions resolved for the current user.

- Every organization member may read campaign conversations beginning with the first successful campaign send.
- Organic conversations and earlier provider history are not imported into the Unibox.
- `can_send_as` is an explicit account-level permission and is never implied by read access.

For an unclaimed legacy account, call `claim_connected_account`, have the user complete the returned provider reconnect URL, then call `get_connected_account_claim_status` with a meaningful wait. Ownership changes only after provider control is verified.

Only the account owner may manage send-as delegates. Resolve a teammate with `list_connected_account_delegate_candidates`, then use `upsert_connected_account_delegate` or `delete_connected_account_delegate`. Confirm before granting send-as because it permits real external campaign sends and replies. Warn that revoking send-as pauses affected future campaign delivery.
