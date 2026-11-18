import {test} from 'node:test';
import assert from 'node:assert/strict';
import {existsSync, readFileSync, readdirSync} from 'node:fs';
import {dirname, join, relative, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {installation} from '../site/install.mjs';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const catalog = JSON.parse(readFileSync(join(root, 'site/catalog.json'), 'utf8'));

function skillFolders(folder) {
  if (existsSync(join(folder, 'SKILL.md'))) return [folder];
  return readdirSync(folder, {withFileTypes: true})
    .filter(entry => entry.isDirectory() && !['.git', 'node_modules', 'site', 'tests'].includes(entry.name) && !entry.name.startsWith('.'))
    .flatMap(entry => skillFolders(join(folder, entry.name)));
}

test('catalog lists every skill folder exactly once with matching versions', () => {
  const folders = skillFolders(root).map(folder => relative(root, folder));
  const paths = catalog.skills.map(skill => skill.sourcePath);
  assert.equal(new Set(paths).size, paths.length, 'duplicate skill');
  assert.deepEqual([...paths].sort(), [...folders].sort());
  for (const skill of catalog.skills) {
    const text = readFileSync(join(root, skill.sourcePath, 'SKILL.md'), 'utf8');
    assert.match(text, new RegExp(`^name:\\s*${skill.id}\\s*$`, 'm'), `${skill.id}: name differs from SKILL.md`);
    assert.equal(text.match(/^\s+version:\s*"?([\d.]+)"?\s*$/m)?.[1], skill.version, `${skill.id}: version differs from SKILL.md`);
    assert.ok(skill.description && skill.example, `${skill.id}: missing description or example`);
  }
});

test('the command contains exactly the selected skills and agents', () => {
  const [skill] = catalog.skills;
  assert.equal(installation([skill], ['codex', 'claude'], catalog.repository).replaceAll(' \\\n  ', ' '),
    `DISABLE_TELEMETRY=1 npx skills add ${catalog.repository} --skill ${skill.id} --agent codex claude-code`);
  assert.ok(installation([skill], ['cursor'], catalog.repository, 'global').endsWith('--global'));
});

test('unsafe catalog values and empty selections are rejected', () => {
  const skills = [catalog.skills[0]];
  installation(catalog.skills, ['codex'], catalog.repository);
  assert.throws(() => installation(skills, ['codex'], 'bad;command/repo'));
  for (const id of ['ok;whoami', '--all', 'a b', 'a\nwhoami']) assert.throws(() => installation([{id}], ['codex'], catalog.repository));
  for (const agent of ['unknown', 'toString', '__proto__']) assert.throws(() => installation(skills, [agent], catalog.repository));
  assert.throws(() => installation([], ['codex'], catalog.repository));
  assert.throws(() => installation(skills, [], catalog.repository));
  assert.throws(() => installation(skills, ['codex'], catalog.repository, 'other'));
});
