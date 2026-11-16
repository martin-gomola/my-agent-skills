import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {installation, usageExample} from '../site/install.mjs';
const catalog = JSON.parse(readFileSync(new URL('../site/catalog.json', import.meta.url)));

test('one command contains exactly the selected skills and target agents', () => {
  const skills = catalog.skills.filter(skill => ['what-to-ask', 'stop-slop'].includes(skill.id));
  const command = installation(skills, ['codex', 'claude', 'cursor', 'antigravity', 'gemini'], catalog.repository);
  assert.equal(command.split('\\\n').map(part => part.trim()).join(' '),
    'DISABLE_TELEMETRY=1 npx skills add martin-gomola/my-agent-skills --skill what-to-ask stop-slop --agent codex claude-code cursor antigravity gemini-cli');
  assert.ok(!command.includes('your-turn-handoff'));
  assert.ok(!command.includes('--global'));
  assert.ok(installation(skills, ['cursor'], catalog.repository, 'global').endsWith('--global'));
  assert.ok(installation(skills, ['cursor'], catalog.repository, 'global').startsWith('DISABLE_TELEMETRY=1 npx skills add '));
  for (const skill of catalog.skills) {
    assert.ok(installation([skill], ['codex'], catalog.repository).includes(`--skill ${skill.id}`));
  }
});

test('empty selections and unsafe command arguments are rejected', () => {
  const skills = [catalog.skills[0]];
  assert.throws(() => installation(skills, ['codex'], 'bad;command/repo'));
  for (const id of ['ok;whoami', '--all', 'a b', 'a\nwhoami']) {
    assert.throws(() => installation([{id}], ['codex'], catalog.repository));
  }
  for (const agent of ['unknown', 'toString', '__proto__']) {
    assert.throws(() => installation(skills, [agent], catalog.repository));
  }
  assert.throws(() => installation([], ['codex'], catalog.repository));
  assert.throws(() => installation(skills, [], catalog.repository));
  assert.throws(() => installation(skills, ['codex'], catalog.repository, 'other'));
});

test('direct skill examples do not use plugin namespaces', () => {
  for (const skill of catalog.skills) {
    assert.equal(usageExample(skill, 'codex'), skill.usage);
    for (const agent of ['', 'claude', 'cursor', 'antigravity', 'gemini']) {
      assert.equal(usageExample(skill, agent), skill.example);
    }
  }
  assert.match(usageExample(catalog.skills.find(skill => skill.id === 'ask'), 'codex'), /^\$ask claude /);
});
