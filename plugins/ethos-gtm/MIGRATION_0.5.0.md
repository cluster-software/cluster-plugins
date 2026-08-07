# Migrating to Ethos 0.5.0

Ethos 0.5.0 makes the hosted MCP server the source of truth for complete skill
workflows. The plugin remains the installation, authentication, and
intent-routing layer, but its local skills now load the current instructions
from MCP resources or the `load_ethos_skill` fallback tool.

## Required client action

1. Update the Ethos plugin to 0.5.0.
2. Keep exactly one active registration for
   `https://api.ethos.hello-cluster.com/mcp`.
3. Remove the legacy Codex `ethos` plugin or `ethos_gtm` MCP registration when
   present; retain `ethos-gtm` and `gtm_ethos`.
4. Start a new chat or task so the client discards cached schemas.

Claude users with an organization-managed Ethos connector should keep that
connector active and leave any duplicate plugin-provided server unauthenticated.
The routing skills use MCP resources when the client exposes them and fall back
to `load_ethos_skill` on clients that do not.
