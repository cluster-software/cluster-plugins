# Ethos MCP skills

This directory contains the complete, server-authored Ethos skill workflows.
The Ethos backend packages these files into immutable MCP resources. It exposes
the router at `skill://ethos/index`, provenance at `skill://ethos/manifest`, and
each complete workflow at `skill://ethos/<name>/SKILL.md`. Clients without MCP
resource discovery use `list_ethos_skills`; clients without resource reads use
`load_ethos_skill` to load a workflow or supporting resource.

The client plugin surface lives at `plugins/ethos-gtm/skills/`. Keeping this
server tree outside the plugin package prevents the complete workflows from
shipping to clients alongside the small routing skills.

Update full workflow instructions here. The automated Ethos synchronization PR
records the exact source commit and file hashes; it never merges automatically.
