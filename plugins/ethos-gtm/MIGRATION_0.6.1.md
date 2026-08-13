# Migrating to Ethos 0.6.1

Ethos 0.6.1 removes CSV browser handoffs from the agent-facing MCP workflow.
Agents now read accessible attachments or local CSV paths, parse the rows, and
use `create_table`, `append_table_rows`, or `create_list` directly.

Update the Ethos plugin before the hosted MCP deployment removes
`create_csv_upload_handoff` and `get_upload_handoff_status`. Older
Legacy client-managed `find-people-at-companies` skills are retired during the
next client upgrade. The manual browser flow remains available temporarily for the
legacy gifting campaign skill.
