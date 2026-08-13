# Migrating to Ethos 0.7.0

Ethos 0.7.0 is a thin hosted-MCP plugin. Workflow guidance now comes from live
MCP resources, so clients receive current instructions without a plugin update.

1. Update the Cluster marketplace and install Ethos 0.7.0.
2. Keep exactly one hosted Ethos MCP connection and complete OAuth if prompted.
3. Start a new chat or task to discard cached plugin components and MCP schemas.
4. Ask Ethos to show the active workspace and confirm that
   `get_workspace_overview` returns the expected organization.

Plugin-local Ethos skills are no longer part of the package. Ask for the desired
workflow in natural language; the client discovers the live resource and the
granular MCP operations it needs.
