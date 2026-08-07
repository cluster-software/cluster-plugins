# Ethos MCP skills

This directory contains the complete, server-authored Ethos skill workflows.
The Ethos backend packages these files into immutable MCP resources and exposes
them through `skill://ethos/...` plus the `load_ethos_skill` fallback tool.

The client plugin surface lives at `plugins/ethos-gtm/skills/`. Keeping this
server tree outside the plugin package prevents the complete workflows from
shipping to clients alongside the small routing skills.

Update full workflow instructions here. The automated Ethos synchronization PR
records the exact source commit and file hashes; it never merges automatically.
