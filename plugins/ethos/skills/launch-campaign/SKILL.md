---
name: launch-campaign
description: Add leads to an Ethos campaign or configure campaign/list operations through MCP.
---

# Launch Campaign

Use Ethos MCP first.

1. If the user already has a campaign, call `add_leads_to_campaign` with a table source or contact IDs.
2. If a list or campaign must be created/configured, call `search_ethos_tools` for the needed atomic operation.
3. Use `call_ethos_tool` for `create_list`, `attach_list_to_campaign`, `create_campaign`, or related operations.

Keep campaign writes explicit. Return campaign ID, lead import ID, counts, and campaign URL.
