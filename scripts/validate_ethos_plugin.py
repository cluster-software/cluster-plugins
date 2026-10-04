import json
from pathlib import Path

PLUGIN_VERSION = "0.7.2"
MCP_URL = "https://api.ethos.hello-cluster.com/mcp"


def main() -> int:
    repository_path = Path(__file__).resolve().parents[1]
    plugin_path = repository_path / "plugins" / "ethos-gtm"
    codex_manifest = json.loads((plugin_path / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    claude_manifest = json.loads((plugin_path / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    claude_marketplace = json.loads(
        (repository_path / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )
    codex_marketplace = json.loads(
        (repository_path / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8")
    )
    mcp_config = json.loads((plugin_path / ".mcp.json").read_text(encoding="utf-8"))

    if (plugin_path / "skills").exists():
        raise ValueError("Cluster 0.7.2 must not ship plugin-local skills")
    if "skills" in codex_manifest:
        raise ValueError("The Codex manifest must not declare plugin-local skills")
    if codex_manifest["name"] != "ethos-gtm" or claude_manifest["name"] != "ethos":
        raise ValueError("Cluster plugin identities changed unexpectedly")
    if codex_manifest["version"] != PLUGIN_VERSION or claude_manifest["version"] != PLUGIN_VERSION:
        raise ValueError(f"Both plugin manifests must use version {PLUGIN_VERSION}")
    if codex_manifest.get("mcpServers") != "./.mcp.json":
        raise ValueError("The Codex plugin must reference the shared hosted MCP configuration")
    if len(codex_manifest.get("interface", {}).get("defaultPrompt", [])) > 3:
        raise ValueError("The Codex manifest supports at most three starter prompts")

    claude_entries = [entry for entry in claude_marketplace["plugins"] if entry["name"] == "ethos"]
    if len(claude_entries) != 1 or claude_entries[0]["version"] != PLUGIN_VERSION:
        raise ValueError(f"The Claude marketplace must expose exactly one Cluster {PLUGIN_VERSION} entry")
    codex_entries = [entry for entry in codex_marketplace["plugins"] if entry["name"] == "ethos-gtm"]
    if len(codex_entries) != 1:
        raise ValueError("The Codex marketplace must expose exactly one ethos-gtm entry")
    if codex_entries[0].get("policy") != {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    }:
        raise ValueError("The Codex marketplace must authenticate the hosted MCP server during installation")

    mcp_servers = mcp_config.get("mcpServers", {})
    if set(mcp_servers) != {"gtm_ethos"} or mcp_servers["gtm_ethos"].get("url") != MCP_URL:
        raise ValueError("The plugin must define exactly one canonical hosted Cluster MCP server")

    for name in ("README.md", "GETTING_STARTED.md"):
        content = (repository_path / name).read_text(encoding="utf-8")
        if "retired" not in content or MCP_URL not in content:
            raise ValueError(f"{name} must explain retirement and direct MCP setup")
        if any(command in content for command in ("plugin marketplace add", "/plugin install", "codex plugin add")):
            raise ValueError(f"{name} must not recommend installing the retired plugin")

    print(f"Validated retired Cluster plugin {PLUGIN_VERSION} and migration guidance")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
