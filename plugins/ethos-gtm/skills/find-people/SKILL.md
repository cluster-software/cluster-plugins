---
name: find-people
description: Find prospects from a natural-language ICP using Ethos MCP.
catalog_title: Find people
catalog_category: Prospecting
catalog_description: Turn a natural-language ICP, search URL, CSV, or company table into a people table.
---

# Find People

Load the current server-authored workflow before acting:

1. Read `skill://ethos/find-people/SKILL.md` when this client exposes MCP
   resources.
2. Otherwise call `load_ethos_skill` with `name="find-people"` and
   `header_only=false`.
3. Follow the returned workflow in full.

This file is only an intent router. If neither loading path is available, ask
the user to update or reconnect Ethos instead of improvising a workflow.
