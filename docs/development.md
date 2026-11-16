# Development

Edit skills only in `skills/<name>/`. Each skill has a separate native adapter
in `plugins/<name>/`, so installing what-to-ask does not enable the handoff.
The skill folders inside plugins are generated snapshots, never authoring copies.

```text
skills/
  what-to-ask/
  your-turn-handoff/
plugins/
  what-to-ask/          # manifests + generated skills/what-to-ask/
  your-turn-handoff/    # manifests + generated skills/your-turn-handoff/
```

After editing a canonical skill, run `make plugins`, then `make test`. Commit the
source and generated snapshots together. Validation rejects snapshot drift.
Plugin identities stay `my-agent-skills` and `your-turn-handoff` for existing
installations; these are distribution identifiers, not alternative skill names.

## Installer page

Start the static chooser locally:

```bash
make dev
```

Open `http://localhost:8983`. Stop the server with `Ctrl+C`; use
`make dev PORT=8984` if the default port is occupied. The command prepares pet
assets before starting the server. The page reads `site/catalog.json`, then generates
one Skills CLI command for the selected skills, agents, and project or global scope.
No backend, analytics, cookies or automatic installation are used by the page.
The external Skills CLI has its own telemetry policy.
`node --test tests/installer.test.mjs` checks selections, scope, command safety,
and usage examples. The site installs skills directly, so examples must not
assume plugin namespaces. Native adapters remain available for existing installs.

The five helpers imported from mythosaur-tools are independent packages. See
[migration and NotebookLM review notes](skill-migration-review.md) for provenance,
dependencies and verification limits. Each plugin contains only its named skill.

Enable GitHub Pages with GitHub Actions as the source. The Pages workflow deploys
after pushes to `main` that change `site/` or the workflow itself. It also supports
manual runs. Changes to `pets/` or `Makefile` also trigger deployment. `make site`
copies canonical pet assets from `pets/` into the ignored `site/pets/` directory
for preview and deployment. The DeeTee section uses the documented Codex pet
install deep link with sprite format v2. The workflow uploads only `site/`; the published site may be public
even while its source repository remains private.

## Validate

The installer-page checks use Node.js 18 or newer. There is no frontend build step.

```sh
git clone https://github.com/martin-gomola/my-agent-skills.git
cd my-agent-skills
make test
```

`make test` uses `uv` and the authoring dependency in `requirements-dev.txt`.
Alternatively install that dependency in a virtual environment, run
`python scripts/validate.py`, then `python -m unittest discover -s tests -v`.
Installation through a client does not require the authoring tools.

Validation checks portable metadata, manifest identity/version consistency, source
checksums, grounded instructions, and common private paths/token patterns. The
behavior cases in `skills/what-to-ask/tests/` are evaluation rubrics, not a claim
that downstream tasks have been executed or that model quality is perfect.

For a local Codex smoke test, use a temporary `CODEX_HOME` and add this repository
as a local marketplace. For Gemini, use a disposable workspace and the native
`--scope workspace` install/list/uninstall commands. Never test replacement against
your real skill registry.

Run `python scripts/smoke_clients.py` to exercise available Codex and Gemini CLI
installers and Antigravity's package validator. The script isolates Codex state
and Gemini configuration, trusts only the disposable Gemini workspace for those
subprocesses, and does not send a model prompt. Registration and metadata discovery
are separate evidence from model activation and successful task execution.
The update checks change fixture content (and the Codex fixture version), then
read back the installed content before uninstalling.
Claude Code and Cursor UI installation must be verified in those clients; JSON
manifest validation alone does not establish that their UI loaded the skill.

## Verification coverage

| Client | Local verification |
| --- | --- |
| Codex | Native local plugin install, cached skill readback, changed-version update and removal |
| Gemini CLI | Workspace install, discovery, changed-content update and removal |
| Antigravity | Native package validation |
| Claude Code and Cursor | Manifest checks; live installation still needs verification in those clients |

Registration and metadata discovery are separate evidence from model activation
and successful task execution. The GitHub install also requires repository access
while the repository is private.

## Consume a pinned version

Consumers can pin this repository as a Git submodule and read `skills/` alongside
their internal source. Pin a reviewed commit; update the submodule deliberately.
Detect duplicate skill names and fail if a required submodule is uninitialized
before replacing installed files. Generated installations are not authoring copies.

## License and provenance

Original instructions and distribution code are [MIT licensed](../LICENSE).
Authoring references and their limitations are recorded in the skill's local
source notes and manifests. Referenced documents retain their own licenses; no
third-party skill implementation or template is bundled.
