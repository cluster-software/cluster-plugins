---
name: manage-unibox
description: Read and reply to Ethos campaign conversations across LinkedIn and email through the unified inbox MCP tools.
catalog_title: Manage unibox
catalog_category: Campaigns
catalog_description: Review and reply to campaign conversations across LinkedIn and email from one merged timeline.
---

# Manage Unibox

Load the current server-authored workflow before acting:

1. Read `skill://ethos/manage-unibox/SKILL.md` when this client exposes MCP
   resources.
2. Otherwise call `load_ethos_skill` with `name="manage-unibox"` and
   `header_only=false`.
3. Follow the returned workflow in full, including every external-send approval
   requirement.

This file is only an intent router. If neither loading path is available, ask
the user to update or reconnect Ethos instead of improvising a workflow.
