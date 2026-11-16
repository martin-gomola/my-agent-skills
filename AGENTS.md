# Skill sources and distribution

- Edit skills in `skills/<name>/` only.
- `plugins/<name>/` contains native manifests and generated skill snapshots.
- Run `make plugins` after changing a skill; commit the source and snapshots together.
- Run `make test` before finishing. Validation rejects stale snapshots.
- Keep each plugin limited to its own skill; the handoff must remain opt-in.
