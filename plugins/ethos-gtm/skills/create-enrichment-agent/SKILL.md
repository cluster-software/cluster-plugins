---
name: create-enrichment-agent
description: Add and run an Ethos enrichment column through MCP.
catalog_title: Create enrichment agent
catalog_category: Enrichment
catalog_description: Create an AI enrichment column, test it on a sample, and run it across the intended rows.
---

# Create Enrichment Agent

Load the current server-authored workflow before acting:

1. Read `skill://ethos/create-enrichment-agent/SKILL.md` when this client exposes
   MCP resources.
2. Otherwise call `load_ethos_skill` with `name="create-enrichment-agent"` and
   `header_only=false`.
3. Follow the returned workflow in full.

This file is only an intent router. If neither loading path is available, ask
the user to update or reconnect Ethos instead of improvising a workflow.
