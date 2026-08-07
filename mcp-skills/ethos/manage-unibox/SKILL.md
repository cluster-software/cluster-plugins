---
name: manage-unibox
description: Read and reply to Ethos campaign conversations across LinkedIn and email through the unified inbox MCP tools.
catalog_title: Manage unibox
catalog_category: Campaigns
catalog_description: Review and reply to campaign conversations across LinkedIn and email from one merged timeline.
---

# Manage Unibox

1. Call `get_workspace_overview` when organization context is ambiguous.
2. Call `search_conversations` with bounded query, campaign, channel, unread, or
   needs-reply filters. Continue only with its cursor.
3. Call `get_conversation` for the selected conversation. Its merged timeline
   and `replyable_threads` are authoritative. Ask the user to choose when the
   recipient, channel, or sender thread is ambiguous.
4. Draft the reply and show the exact recipient, thread/channel, and text.
   `send_reply` sends a real external message and may stop campaign automation;
   obtain explicit approval immediately before calling it.
5. Generate one idempotency key for that exact conversation, thread, and text.
   Reuse it for an exact retry; use a new key only for a new intentional send.
6. Treat `pending` or unknown delivery as uncertain. Never blindly resend or
   create a new key; call `get_conversation` to reconcile first. After a failed
   delivery, require approval before a new attempt.

Plain-text replies on existing replyable threads are supported. Do not claim
support for attachments, cold sends, or creating a new thread.
