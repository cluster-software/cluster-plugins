---
name: enrich-contact-info
description: Enrich work emails and phone numbers in an Ethos people table using MCP.
catalog_title: Enrich contact info
catalog_category: Enrichment
catalog_description: Find work emails and phone numbers for selected people-table rows.
---

# Enrich Contact Info

Load the current server-authored workflow before acting:

1. Read `skill://ethos/enrich-contact-info/SKILL.md` when this client exposes MCP
   resources.
2. Otherwise call `load_ethos_skill` with `name="enrich-contact-info"` and
   `header_only=false`.
3. Follow the returned workflow in full.

This file is only an intent router. If neither loading path is available, ask
the user to update or reconnect Ethos instead of improvising a workflow.
