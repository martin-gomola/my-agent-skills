"""Validate portable skill sources and the thin native-client manifests."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import yaml
from sync_plugins import sync

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json", ".cursor-plugin/plugin.json")
MARKETS = (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json", ".cursor-plugin/marketplace.json")


def validate_skill(folder: Path) -> None:
    if not (folder / "LICENSE").is_file():
        raise ValueError(f"{folder.name}: standalone installations must include a license")
    text = (folder / "SKILL.md").read_text()
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError(f"{folder.name}: missing frontmatter")
    metadata = yaml.safe_load(parts[1])
    if not isinstance(metadata, dict) or not {"name", "description"} <= set(metadata) or set(metadata) - {"name", "description", "metadata"}:
        raise ValueError(f"{folder.name}: expected portable name and description")
    if metadata["name"] != folder.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", folder.name):
        raise ValueError(f"{folder.name}: invalid skill name")
    if not isinstance(metadata["description"], str) or not 1 <= len(metadata["description"]) <= 1024:
        raise ValueError(f"{folder.name}: invalid description")
    for fixture in ("eval.yaml", "triggers.yaml"):
        data = yaml.safe_load((folder / "tests" / fixture).read_text())
        if data.get("skill") != folder.name:
            raise ValueError(f"{folder.name}: incorrect fixture identity")
    source_manifest = yaml.safe_load((folder / "sources.yaml").read_text()) if (folder / "sources.yaml").exists() else {"sources": []}
    for source in source_manifest["sources"]:
        target = (folder / source["locator"]).resolve()
        if not target.is_relative_to(folder.resolve()):
            raise ValueError("source path escapes skill")
        if hashlib.sha256(target.read_bytes()).hexdigest() != source["sha256"]:
            raise ValueError("source checksum mismatch")
    grounding = yaml.safe_load((folder / "grounding.yaml").read_text()) if (folder / "grounding.yaml").exists() else {"claims": []}
    for claim in grounding["claims"]:
        if claim["instruction"] not in text:
            raise ValueError(f"{folder.name}: stale grounded instruction")


def validate(root: Path = ROOT) -> None:
    default_plugin = root / 'plugins/what-to-ask'
    manifests = [json.loads((default_plugin / path).read_text()) for path in MANIFESTS]
    identities = {(item["name"], item["version"]) for item in manifests}
    if len(identities) != 1 or manifests[0]["name"] != "my-agent-skills":
        raise ValueError("plugin names or versions differ")
    for path in MARKETS:
        data = json.loads((root / path).read_text())
        expected_plugins = {('my-agent-skills' if p.name == 'what-to-ask' else p.name): p.name for p in (root / 'skills').iterdir() if p.is_dir()}
        if data["name"] != "my-agent-skills" or {entry["name"] for entry in data["plugins"]} != set(expected_plugins) or len(data["plugins"]) != len(expected_plugins):
            raise ValueError(f"{path}: incorrect marketplace")
        for entry in data["plugins"]:
            source = entry["source"]
            location = source["path"] if isinstance(source, dict) else source
            expected = "./plugins/" + expected_plugins[entry['name']]
            if location != expected:
                raise ValueError(f"{path}: incorrect plugin source")
    handoff = root / "plugins/your-turn-handoff"
    handoff_manifests = [json.loads((handoff / path).read_text()) for path in MANIFESTS]
    if len({(item['name'], item['version']) for item in handoff_manifests}) != 1 or handoff_manifests[0]['name'] != 'your-turn-handoff':
        raise ValueError('handoff plugin names or versions differ')
    for skill in sorted((root / "skills").iterdir()):
        if skill.is_dir():
            validate_skill(skill)
            adapters = [json.loads((root / 'plugins' / skill.name / path).read_text()) for path in MANIFESTS]
            if len({(item['name'], item['version']) for item in adapters}) != 1:
                raise ValueError(f'{skill.name}: plugin names or versions differ')
    catalog = json.loads((root / 'site/catalog.json').read_text())
    for skill in catalog['skills']:
        target = (root / skill['sourcePath']).resolve()
        if not target.is_relative_to(root.resolve()) or not (target / 'SKILL.md').is_file():
            raise ValueError('installer references an invalid skill')
        package = root / skill['pluginPath']
        plugin_manifest = json.loads((package / 'plugin.json').read_text())
        if plugin_manifest['name'] != skill['plugin'] or target != (root / 'skills' / skill['id']).resolve() or package != root / 'plugins' / skill['id']:
            raise ValueError('installer skill and plugin do not match')
        if skill.get('version') != plugin_manifest['version']:
            raise ValueError('installer version and plugin manifest do not match')
    sync(root, check=True)
    for path in root.rglob("*"):
        if not path.is_file() or any(part in {".git", "__pycache__", "tmp", "dist", ".venv"} for part in path.relative_to(root).parts):
            continue
        text = path.read_text(errors="replace")
        if re.search(r"/(?:Users|home)/[A-Za-z0-9_.-]+/|\bgh[pousr]_[A-Za-z0-9]{20,}|\bsk-[A-Za-z0-9]{20,}", text):
            raise ValueError(f"private path or token in {path.relative_to(root)}")
        if path.name == ".env" or path.suffix == ".env":
            raise ValueError("environment files must not be packaged")


if __name__ == "__main__":
    validate()
    print("Skill sources, provenance, public-content scan and client manifests passed.")
