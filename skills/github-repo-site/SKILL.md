---
name: github-repo-site
description: Builds and publishes a static GitHub Pages site for any GitHub repository, explaining what the project does, who it is for, how to install and start, with copyable commands, examples and links drawn only from the repository. Use to make a project page, landing page, homepage or GitHub Pages site for a repo, refresh an outdated one, or add an installer page that lets visitors pick skills from a SKILL.md skills repository. Avoid for multi-page documentation generators such as MkDocs or Docusaurus, personal blogs, marketing copy without a repository, or hosting outside GitHub Pages.
metadata:
  version: "0.1.0"
  trigger: Creating or updating a GitHub Pages site for a repository
---

# GitHub Repo Site

Turn a repository into a single static page that answers three questions within a minute: what is this, is it for me, and how do I start. Every claim on the page comes from the repository. The page has no build step, backend, analytics, cookies, or third-party scripts.

## Contents

- Gather facts
- Choose the page type
- Build a project page
- Build a skill installer page
- Check and preview
- Publish
- Completion report

## 1. Gather facts

Inspect the repository before writing anything.

1. Read the GitHub `owner/repo` slug from `git remote get-url origin`. If there is no GitHub remote, stop and ask; do not guess it.
2. Read the README, the license, the package manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod` or similar), `docs/`, `examples/`, existing screenshots, and the default branch. Run `gh release list --limit 5` and `gh api repos/<owner/repo>/pages` when `gh` is available.
3. Write a short fact list: name, one-line purpose, audience, requirements, install command, first-run command, three to six capabilities, one real example, project status, license, and links. Note the source file for each fact.
4. Ask the user only for facts the repository does not contain and the page needs, such as the intended audience when the README never says. Leave a section out instead of filling it with guesses.
5. If `site/`, `docs/` or a Pages workflow already exists, ask before replacing it. When refreshing, keep working content and correct only what is outdated.

Do not invent features, benchmarks, user counts, testimonials, badges, or comparisons. Copy commands verbatim from the repository. State the real status, such as experimental or archived, when the repository says so.

## 2. Choose the page type

- **Project page**, the default: for libraries, CLIs, apps, datasets, templates and other projects.
- **Skill installer page**: when the repository's purpose is distributing skills, meaning it contains folders with a `SKILL.md`, and visitors should pick which skills to install.

## 3. Build a project page

Copy [assets/project/index.html](assets/project/index.html) to `site/index.html`, [assets/project/copy.js](assets/project/copy.js) to `site/copy.js`, and [assets/style.css](assets/style.css) to `site/style.css`. Replace every `{{PLACEHOLDER}}` with facts from step 1.

Write for a visitor who has never heard of the project:

- **Heading:** what the visitor gets, in plain words, not the project's internal name alone.
- **Lead:** one sentence that names the audience and the problem it solves.
- **Quick start:** requirements, then the shortest command sequence from the README that produces a visible result. Use one `<pre data-copy>` per command so each gets a copy button.
- **What it does:** three to six concrete capabilities. Repeat the `<li>` for each one and remove the section if the README lists none.
- **Example:** one real input and output, code sample, or screenshot from the repository. Store images under `site/` with descriptive `alt` text and keep each under about 300 KB.
- **Learn more:** documentation, issues, releases, changelog, and contributing links that exist.
- **Footer:** the license name and the repository link.

Use relative paths for local files because project sites are served from `https://<owner>.github.io/<repo>/`. Write the page in the README's language unless the user asks otherwise. Keep the template's accessibility features: `lang`, a meta description, heading order, focus outlines, and the light and dark color schemes.

## 4. Build a skill installer page

Copy these assets without changing their logic:

| Asset | Destination |
| --- | --- |
| [assets/skill-installer/index.html](assets/skill-installer/index.html) | `site/index.html` |
| [assets/skill-installer/install.mjs](assets/skill-installer/install.mjs) | `site/install.mjs` |
| [assets/style.css](assets/style.css) | `site/style.css` |
| [assets/skill-installer/installer.test.mjs](assets/skill-installer/installer.test.mjs) | `tests/installer.test.mjs` |

Create `site/catalog.json` from [assets/skill-installer/catalog.example.json](assets/skill-installer/catalog.example.json) with the verified `repository` slug, a page `title`, and one entry per skill folder. Each entry needs the following fields:

- `id` and `label`: the frontmatter `name`, which must match the folder name.
- `sourcePath`: the folder path relative to the repository root.
- `version`: `metadata.version` when the skill has one; otherwise omit it.
- `description`: one line, at most about 60 characters, saying what the skill does for the visitor.
- `example`: one realistic sentence a visitor can paste into a chat to try the skill.

`install.mjs` validates the repository slug, every skill id, every agent id and the scope, and rejects the whole catalog when one value is invalid. Keep that validation. The command contains only the selected skills, starts with `DISABLE_TELEMETRY=1` so the Skills CLI run sends no telemetry, and the page never runs it. Keep the agent list in `install.mjs` and `index.html` identical.

When the repository is already pushed, confirm the Skills CLI sees the skills with `npx skills add <owner/repo> --list`. When skills are later added, removed or versioned, update only `site/catalog.json`.

## 5. Check and preview

Run the checks and fix every failure before continuing:

```bash
node <this-skill>/scripts/check_site.mjs site
node --test tests/installer.test.mjs   # installer page only
python3 -m http.server 8983 --bind 127.0.0.1 --directory site
```

[scripts/check_site.mjs](scripts/check_site.mjs) needs Node.js 18 or newer and no packages. It reports unfilled placeholders, missing `lang`, title or description, images without `alt`, third-party scripts, missing local files, and root-absolute paths that break on project sites. The installer test fails when the catalog misses a skill folder, lists one twice, or has a version that differs from `SKILL.md`.

Open `http://127.0.0.1:8983` at desktop and mobile widths and in dark mode. Copy one command and confirm it matches the README. Opening `index.html` straight from disk can break the installer page, because it fetches `catalog.json`.

## 6. Publish

Copy [assets/pages.yml](assets/pages.yml) to `.github/workflows/pages.yml` and change `branches: [main]` when the default branch differs. The workflow deploys `site/` on pushes to that branch.

GitHub Pages must use **GitHub Actions** as its source. That setting and the repository homepage change the user's repository, so ask before running:

```bash
gh api -X POST repos/<owner/repo>/pages -f build_type=workflow
gh repo edit <owner/repo> --homepage https://<owner>.github.io/<repo>/
```

Use `-X PUT repos/<owner/repo>/pages` instead of `POST` when Pages already exists with another source. If the user prefers, tell them to choose **Settings → Pages → Source → GitHub Actions**. Do not commit or push unless the user asks. Add the page URL near the top of the README.

## 7. Completion report

Report the page type, the page URL or the pending publish step, which facts came from which files, the sections you left out and why, the check results, and any check that could not run, such as `--list` before the first push.
