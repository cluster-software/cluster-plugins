# Ethos MCP skills

This directory contains the complete, server-authored Ethos skill workflows.
The Ethos backend packages these files into immutable MCP resources and exposes
them through `skill://ethos/...` plus the `load_ethos_skill` fallback tool.

The neighboring `skills/` directory is the client plugin surface. It may contain
small routing skills, but it must not be used to build the server bundle.

Update full workflow instructions here. The automated Ethos synchronization PR
records the exact source commit and file hashes; it never merges automatically.
