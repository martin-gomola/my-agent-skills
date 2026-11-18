const agentIds = {codex: 'codex', claude: 'claude-code', cursor: 'cursor', antigravity: 'antigravity', gemini: 'gemini-cli'};
const name = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

export function installation(skills, agents, repository, scope = 'project') {
  if (!/^[a-zA-Z0-9_.-]+\/[a-zA-Z0-9_.-]+$/.test(repository)) throw Error('Invalid repository');
  if (!skills.length || skills.some(skill => !name.test(skill.id))) throw Error('Invalid skills');
  if (!agents.length || agents.some(agent => !Object.hasOwn(agentIds, agent))) throw Error('Unknown agent');
  if (!['project', 'global'].includes(scope)) throw Error('Invalid scope');
  const parts = [`DISABLE_TELEMETRY=1 npx skills add ${repository}`, `--skill ${skills.map(skill => skill.id).join(' ')}`, `--agent ${agents.map(agent => agentIds[agent]).join(' ')}`];
  if (scope === 'global') parts.push('--global');
  return parts.join(' \\\n  ');
}

if (typeof document !== 'undefined') {
  const byId = id => document.getElementById(id);
  let catalog;

  function render() {
    const ids = [...document.querySelectorAll('input[name="skill"]:checked')].map(input => input.value);
    const skills = catalog.skills.filter(skill => ids.includes(skill.id));
    const agents = [...document.querySelectorAll('input[name="agent"]:checked')].map(input => input.value);
    const scope = document.querySelector('input[name="scope"]:checked').value;
    const ready = skills.length > 0 && agents.length > 0;
    byId('copy').textContent = 'Copy command';
    byId('copy').disabled = !ready;
    byId('install-content').hidden = !ready;
    byId('status').textContent = '';
    byId('commands').textContent = ready ? installation(skills, agents, catalog.repository, scope) : '';
    byId('where').textContent = ready
      ? `Run in ${scope === 'project' ? 'your project folder' : 'your terminal'}, then start a new agent chat.`
      : !skills.length ? 'Choose one or more skills to get started.' : 'Choose the agents you use to get your install command.';
    byId('examples').replaceChildren(...skills.map(skill => {
      const example = document.createElement('pre');
      example.tabIndex = 0;
      example.textContent = skill.example;
      return example;
    }));
  }

  document.querySelector('.choices').addEventListener('change', () => { if (catalog) render(); });
  byId('copy').addEventListener('click', async () => {
    const command = byId('commands').textContent;
    try {
      await navigator.clipboard.writeText(command);
      byId('copy').textContent = 'Copied';
      byId('status').textContent = 'Command copied. Paste it in your terminal.';
    } catch {
      const range = document.createRange();
      range.selectNodeContents(byId('commands'));
      getSelection().removeAllRanges();
      getSelection().addRange(range);
      byId('status').textContent = 'Clipboard unavailable. Copy the selected command manually.';
    }
  });

  fetch('catalog.json').then(response => {
    if (!response.ok) throw Error('Catalog unavailable');
    return response.json();
  }).then(data => {
    if (!data.skills?.length) throw Error('Empty catalog');
    installation(data.skills, Object.keys(agentIds), data.repository);
    catalog = data;
    document.title = data.title;
    byId('title').textContent = data.title;
    byId('repository').href = `https://github.com/${data.repository}`;
    byId('repository').textContent = data.repository;
    byId('skills').replaceChildren(...data.skills.map(skill => {
      const label = document.createElement('label');
      const input = document.createElement('input');
      input.type = 'checkbox'; input.name = 'skill'; input.value = skill.id;
      const text = document.createElement('span');
      const title = document.createElement('strong'); title.textContent = skill.label;
      const description = document.createElement('small'); description.textContent = skill.description;
      if (skill.version) label.title = `${skill.label} v${skill.version}`;
      text.append(title, description); label.append(input, text);
      return label;
    }));
    render();
  }).catch(() => {
    byId('skills').textContent = 'Skill list unavailable.';
    byId('where').textContent = 'Could not load the skill list. Reload this page to try again.';
  });
}
