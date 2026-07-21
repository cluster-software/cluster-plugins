---
name: manage-unibox
description: Read and reply to Ethos campaign conversations across LinkedIn and email through the unified inbox MCP tools.
catalog_title: Manage unibox
catalog_category: Campaigns
catalog_description: Review and reply to campaign conversations across LinkedIn and email from one merged timeline.
---

# Manage Unibox

Use Ethos MCP first. The unibox tools are searchable: load them with `search_ethos_tools` (query "unibox inbox LinkedIn email") and invoke them with `call_ethos_tool`.

## Preconditions

1. Confirm the organization with `get_current_ethos_org`; call `switch_ethos_org` first if the user means another authorized organization.
2. Default to campaign conversations. Set `include_all=true` only when the user explicitly asks to include organic conversations from every connected LinkedIn and email account, and require a `since` timestamp to bound provider history through now. All-mode should not be used speculatively.

## Read conversations

1. Call `list_unibox_conversations` with `include_all=false`. To include organic conversations, set `include_all=true` and provide the required `since` timestamp; this bounds provider history from that timestamp through now.
2. Pass the returned `data.cursor` to retrieve the next page. Each page hydrates at most one provider page per connected account.
3. Identify the desired conversation by contact, company, campaign, preview, or channel. If the result is ambiguous, ask the user before sending anything.
4. Call `get_unibox_conversation` with its `conversation_id` and the same `include_all` and `since` values. Its timeline merges LinkedIn and email chronologically. Continue with `data.cursor` when older messages are needed.
5. Choose a thread with `is_replyable=true`. When multiple threads are available, honor the user's requested channel and sender account; otherwise present the available channel/account choices before sending.

## Send a reply

`send_unibox_message` is destructive: it sends a real provider message and takes over the contact from campaign automation. Confirm the exact recipient, channel or sender thread, and text with the user before calling it.

1. Generate one client idempotency key for the intended conversation, thread, and text. Reuse that same key for every retry of that exact send attempt.
2. Call `send_unibox_message` with `conversation_id`, `thread_id`, `text`, and `idempotency_key`.
3. Report the normalized delivery state, stopped campaign IDs, and any already-running-send warnings. Manual takeover remains in effect even if provider delivery fails.
4. Treat `pending` or `unknown` as uncertain delivery. Do not generate a new idempotency key or blindly retry; first retrieve the conversation again and ask the user before attempting reconciliation or another send.
5. A `failed` result may be retried only after the user approves the same or edited text. Use a new key for a new intentional attempt.

## Limits

- Version one sends plain text replies only. It does not support attachments, mark-read controls, cold sends, or creating a new provider thread.
- A reply must target an existing internal `thread_id`; email replies inherit the provider thread subject and LinkedIn replies stay in the existing chat.
- The default view omits organic conversations and every message before the first successful Ethos campaign action for the contact.
