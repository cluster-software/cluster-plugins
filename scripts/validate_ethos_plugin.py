import json
import re
from pathlib import Path

PLUGIN_VERSION = "0.7.0"
MCP_URL = "https://api.ethos.hello-cluster.com/mcp"
FORBIDDEN_AGENT_GUIDANCE = (
    re.compile(r"\bethos-cli\b", re.IGNORECASE),
    re.compile(r"\bCLI\b"),
    re.compile(r"\bcommand-line\b", re.IGNORECASE),
    re.compile(r"(?:\$|/)ethos:setup\b", re.IGNORECASE),
    re.compile(r"\bNode\.js\b", re.IGNORECASE),
    re.compile(r"\bnpm\s+install\b", re.IGNORECASE),
)


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
        raise ValueError("Ethos 0.7.0 must not ship plugin-local skills")
    if "skills" in codex_manifest:
        raise ValueError("The Codex manifest must not declare plugin-local skills")
    if codex_manifest["name"] != "ethos-gtm" or claude_manifest["name"] != "ethos":
        raise ValueError("Ethos plugin identities changed unexpectedly")
    if codex_manifest["version"] != PLUGIN_VERSION or claude_manifest["version"] != PLUGIN_VERSION:
        raise ValueError(f"Both plugin manifests must use version {PLUGIN_VERSION}")
    if codex_manifest.get("mcpServers") != "./.mcp.json":
        raise ValueError("The Codex plugin must reference the shared hosted MCP configuration")
    if len(codex_manifest.get("interface", {}).get("defaultPrompt", [])) > 3:
        raise ValueError("The Codex manifest supports at most three starter prompts")

    claude_entries = [entry for entry in claude_marketplace["plugins"] if entry["name"] == "ethos"]
    if len(claude_entries) != 1 or claude_entries[0]["version"] != PLUGIN_VERSION:
        raise ValueError(f"The Claude marketplace must expose exactly one Ethos {PLUGIN_VERSION} entry")
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
        raise ValueError("The plugin must define exactly one canonical hosted Ethos MCP server")

    agent_facing_paths = [
        repository_path / "README.md",
        repository_path / "GETTING_STARTED.md",
        repository_path / ".claude-plugin" / "marketplace.json",
        repository_path / ".agents" / "plugins" / "marketplace.json",
        *sorted(path for path in plugin_path.rglob("*") if path.is_file()),
    ]
    for path in agent_facing_paths:
        content = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_AGENT_GUIDANCE:
            if pattern.search(content):
                raise ValueError(f"{path.relative_to(repository_path)} contains prohibited guidance: {pattern.pattern}")

    print(f"Validated thin Ethos plugin {PLUGIN_VERSION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
