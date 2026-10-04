# Connect to Cluster — the plugin is retired

Cluster was formerly known as Ethos. Both names refer to the same product.
The Cluster plugin marketplace is retired. Use a direct MCP connection or the
standalone CLI; neither requires this plugin repository.

## Connect an AI client through MCP

1. Open the client's remote MCP server or connector setup.
2. Use `https://api.ethos.hello-cluster.com/mcp` as the server URL, with
   streamable HTTP transport and OAuth authentication.
3. Approve access to the intended Cluster workspace in the browser.
4. Start a fresh session so the client loads the tools and resources.
5. Ask: `Use Cluster to confirm my active workspace with get_workspace_overview.`
   This is a read-only check.

Reuse an existing direct connection at that URL. Do not add a duplicate simply
because its name is Ethos, GTM Cluster, `gtm_ethos`, or `ethos_gtm`.
The hosted server provides the current tools and workflow guidance as MCP
resources; there are no local skills to install.

## Migrate an existing plugin installation

1. Inspect the client's installed plugins and MCP connections. Identify which
   connection is owned by the retired Cluster plugin and whether a separate
   direct connection already exists at the URL above.
2. If a direct connection already exists, verify it using the read-only check
   above. Otherwise, record the MCP URL and intended workspace before removing
   the plugin, then create the direct connection using the setup steps above.
3. Remove only the retired Cluster plugin (`ethos` in Claude or `ethos-gtm` in
   Codex; older installations may use `ethos`). Removing it may also remove its
   bundled MCP connection. Do not remove unrelated plugins or servers.
4. Remove the `cluster-plugins` marketplace from the client if it is no longer
   needed. Keep exactly one enabled direct Cluster connection at the MCP URL.
5. Start a fresh session and verify the direct connection again. If authorization
   was removed with the plugin, complete OAuth again for the intended workspace.

Archiving this repository does not remove installed plugins, revoke OAuth, or
stop the hosted MCP service. Do not assume a plugin-owned connection will survive
uninstallation; the final direct-connection check is required.

## Use the standalone CLI

Install or update the supported CLI, then authenticate through the browser:

```bash
npm install -g ethos-cli@latest
ethos auth login
ethos auth status
```

The CLI is independent of MCP client setup. Installing it does not install a
plugin or configure an AI client's MCP connection. See the
[CLI package and documentation](https://www.npmjs.com/package/ethos-cli).

Older CLI versions may recommend this marketplace through `ethos skills install`.
That recommendation is obsolete; use direct MCP setup instead. Workflow guidance
is served by MCP resources. To inspect or remove local skill files installed by
an older CLI, use:

```bash
ethos skills list
ethos skills remove
```

Only run the removal command when you intend to remove those legacy local skills.
It is separate from uninstalling a plugin or removing a client MCP connection.

## Repository status

The plugin is retired and will receive no new releases. Existing manifests and
historical migration files are preserved for reference. Follow this page for
current setup; do not follow plugin installation steps in historical documents.
