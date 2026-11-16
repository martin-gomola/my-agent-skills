"""Exercise available native installers using disposable client/workspace state.

This tests registration and discovered metadata, not model activation or task quality.
"""
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(args, cwd, env):
    result = subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True, timeout=60)
    if result.returncode:
        raise RuntimeError(f"{args[0]} {args[1]} failed: {result.stderr or result.stdout}")
    return result.stdout


def smoke():
    with tempfile.TemporaryDirectory(prefix="agent-skills-clients-") as temporary:
        base = Path(temporary)
        if shutil.which("codex"):
            state = base / "codex"
            state.mkdir()
            env = {**os.environ, "CODEX_HOME": str(state)}
            package = base / "codex-package"
            shutil.copytree(ROOT, package, ignore=shutil.ignore_patterns(".git", "tmp", "dist", "__pycache__", ".venv"))
            run(["codex", "plugin", "marketplace", "add", str(package)], base, env)
            run(["codex", "plugin", "add", "my-agent-skills@my-agent-skills"], base, env)
            catalog = run(["codex", "plugin", "list", "--marketplace", "my-agent-skills", "--json"], base, env)
            assert "my-agent-skills" in catalog and "true" in catalog, catalog
            assert not any(item['pluginId'] == 'your-turn-handoff@my-agent-skills' for item in json.loads(catalog)['installed'])
            installed = list((state / "plugins/cache").rglob("skills/what-to-ask/SKILL.md"))
            assert installed and all(path.read_bytes() == (ROOT / "skills/what-to-ask/SKILL.md").read_bytes() for path in installed)
            for name in ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json", ".cursor-plugin/plugin.json"):
                manifest = package / 'plugins/what-to-ask' / name
                data = json.loads(manifest.read_text())
                data["version"] = "0.1.1"
                manifest.write_text(json.dumps(data))
            updated = package / "plugins/what-to-ask/skills/what-to-ask/SKILL.md"
            updated.write_text(updated.read_text() + "\nUpdate smoke marker.\n")
            run(["codex", "plugin", "add", "my-agent-skills@my-agent-skills"], base, env)
            assert any("Update smoke marker." in path.read_text() for path in (state / "plugins/cache").rglob("skills/what-to-ask/SKILL.md"))
            run(["codex", "plugin", "add", "your-turn-handoff@my-agent-skills"], base, env)
            handoffs = list((state / "plugins/cache/my-agent-skills/your-turn-handoff").rglob("SKILL.md"))
            assert len(handoffs) == 1 and handoffs[0].read_bytes() == (ROOT / "skills/your-turn-handoff/SKILL.md").read_bytes()
            run(["codex", "plugin", "remove", "your-turn-handoff@my-agent-skills"], base, env)
            run(["codex", "plugin", "remove", "my-agent-skills@my-agent-skills"], base, env)
            assert not list((state / "plugins/cache").rglob("skills/what-to-ask/SKILL.md"))
            print("Codex: native install, skill readback, changed-version update and removal passed")
        else:
            print("Codex: skipped (CLI unavailable)")
        if shutil.which("gemini"):
            workspace = base / "gemini-workspace"
            workspace.mkdir()
            env = {**os.environ, "GEMINI_CLI_HOME": str(base / "gemini-state"),
                   "GEMINI_CLI_TRUST_WORKSPACE": "true"}
            source = base / "gemini-source/what-to-ask"
            shutil.copytree(ROOT / "skills/what-to-ask", source)
            args = ["gemini", "skills", "install", str(source), "--scope", "workspace", "--consent"]
            run(args, workspace, env)
            found = run(["gemini", "skills", "list", "--all"], workspace, env)
            assert "what-to-ask" in found
            gemini_installed = list(workspace.rglob("SKILL.md"))
            assert len(gemini_installed) == 1 and gemini_installed[0].read_bytes() == (ROOT / "skills/what-to-ask/SKILL.md").read_bytes()
            updated = source / "SKILL.md"
            updated.write_text(updated.read_text() + "\nUpdate smoke marker.\n")
            run(args, workspace, env)
            assert "Update smoke marker." in gemini_installed[0].read_text()
            run(["gemini", "skills", "uninstall", "what-to-ask", "--scope", "workspace"], workspace, env)
            assert not list(workspace.rglob("SKILL.md"))
            handoff = ROOT / 'skills/your-turn-handoff'
            run(['gemini','skills','install',str(handoff),'--scope','workspace','--consent'], workspace, env)
            assert 'your-turn-handoff' in run(['gemini','skills','list','--all'], workspace, env)
            assert any(path.read_bytes() == (handoff / 'SKILL.md').read_bytes() for path in workspace.rglob('SKILL.md'))
            run(['gemini','skills','uninstall','your-turn-handoff','--scope','workspace'],workspace,env)
            assert not list(workspace.rglob('SKILL.md'))
            print("Gemini CLI: workspace install, discovery, changed-content update and removal passed")
        else:
            print("Gemini CLI: skipped (CLI unavailable)")
        if shutil.which("agy"):
            run(["agy", "plugin", "validate", str(ROOT / 'plugins/what-to-ask')], base, os.environ.copy())
            run(["agy", "plugin", "validate", str(ROOT / "plugins/your-turn-handoff")], base, os.environ.copy())
            print("Antigravity: native package validation passed (no live-registry installation)")
        else:
            print("Antigravity: skipped (CLI unavailable)")


if __name__ == "__main__":
    smoke()
