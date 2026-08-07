---
name: manage-workflows
description: Create, inspect, update, activate, or pause Ethos signal-driven workflows through MCP. Use when a user wants a standing automation that enriches matches, finds people, adds rows or campaign leads, or sends a notification.
catalog_title: Manage workflows
catalog_category: Workflows
catalog_description: Build and operate durable signal-driven Ethos automations.
---

# Manage Workflows

Load the current server-authored workflow before acting:

1. Read `skill://ethos/manage-workflows/SKILL.md` when this client exposes MCP
   resources.
2. Otherwise call `load_ethos_skill` with `name="manage-workflows"` and
   `header_only=false`.
3. Follow the returned workflow in full, including every workflow-state approval
   requirement.

This file is only an intent router. If neither loading path is available, ask
the user to update or reconnect Ethos instead of improvising a workflow.
