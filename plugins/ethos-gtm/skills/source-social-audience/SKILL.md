---
name: source-social-audience
description: Source followers, connections, or post engagers from a LinkedIn company page, X account, or LinkedIn post into an Ethos table. Use when a user asks for a competitor's followers, a social audience, page followers, account followers, connections, fans, reactors, or commenters.
catalog_title: Source social audience
catalog_category: Prospecting
catalog_description: Pull a native LinkedIn or X audience into an Ethos people table without browser scraping.
---

# Source Social Audience

Load the current server-authored workflow before acting:

1. Read `skill://ethos/source-social-audience/SKILL.md` when this client exposes
   MCP resources.
2. Otherwise call `load_ethos_skill` with `name="source-social-audience"` and
   `header_only=false`.
3. Follow the returned workflow in full, including its native-source,
   provenance, and credit-approval requirements.

This file is only an intent router. If neither loading path is available, ask
the user to update or reconnect Ethos instead of browser-scraping or
approximating the requested audience.
