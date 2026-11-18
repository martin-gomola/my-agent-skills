const agentIds = {codex: 'codex', claude: 'claude-code', cursor: 'cursor', antigravity: 'antigravity', gemini: 'gemini-cli'};

export function installation(skills, agents, repository, scope = 'project') {
  if (!/^[a-zA-Z0-9_.-]+\/[a-zA-Z0-9_.-]+$/.test(repository)) throw Error('Invalid repository');
  if (!skills.length || skills.some(skill => !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(skill.id))) throw Error('Invalid skills');
  if (!agents.length || agents.some(agent => !Object.hasOwn(agentIds, agent))) throw Error('Unknown agent');
  if (!['project', 'global'].includes(scope)) throw Error('Invalid scope');
  const parts = [`DISABLE_TELEMETRY=1 npx skills add ${repository}`, `--skill ${skills.map(skill => skill.id).join(' ')}`, `--agent ${agents.map(agent => agentIds[agent]).join(' ')}`];
  if (scope === 'global') parts.push('--global');
  return parts.join(' \\\n  ');
}

export function usageExample(skill, agent) {
  return agent === 'codex' ? skill.usage : skill.example;
}

if (typeof document !== 'undefined') {
  const byId = id => document.getElementById(id);
  let catalog;
  let resetCopy;
  function render() {
    clearTimeout(resetCopy);
    byId('copy').textContent = 'Copy command';
    const ids = [...document.querySelectorAll('input[name="skill"]:checked')].map(input => input.value);
    const skills = catalog.skills.filter(skill => ids.includes(skill.id));
    const agents = [...document.querySelectorAll('input[name="agent"]:checked')].map(input => input.value);
    const scope = document.querySelector('input[name="scope"]:checked').value;
    const ready = skills.length > 0 && agents.length > 0;
    byId('install-panel').dataset.state = ready ? 'ready' : 'empty';
    byId('copy').disabled = !ready;
    byId('install-content').hidden = !ready;
    byId('your-turn-link').hidden = !ids.includes('your-turn-handoff');
    byId('status').textContent = '';
    if (catalog.bundle) {
      const bundle = catalog.bundle.steps.flatMap(step => step.skills);
      const selected = bundle.length === ids.length && bundle.every(id => ids.includes(id));
      byId('flow-select').setAttribute('aria-pressed', selected);
      byId('flow-select').textContent = selected ? 'Bundle selected' : `Select ${bundle.length} skills`;
    }
    byId('commands').textContent = ready ? installation(skills, agents, catalog.repository, scope) : '';
    byId('summary').hidden = !ready;
    byId('summary').textContent = ready
      ? `${skills.length} ${skills.length === 1 ? 'skill' : 'skills'} · ${agents.length} ${agents.length === 1 ? 'agent' : 'agents'} · ${scope === 'project' ? 'one project' : 'all projects'}`
      : '';
    byId('where').textContent = ready
      ? `Run in ${scope === 'project' ? 'your project folder' : 'your terminal'}.`
      : !skills.length ? 'Choose one or more skills to get started.' : 'Choose the agents you use to get your install command.';
    byId('examples').replaceChildren();
    for (const skill of skills) {
      const example = document.createElement('pre'); example.tabIndex = 0;
      example.textContent = usageExample(skill, agents.length === 1 ? agents[0] : '');
      byId('examples').append(example);
    }
  }
  document.querySelector('.choices').addEventListener('change', () => { if (catalog) render(); });
  byId('copy').addEventListener('click', async () => {
    const command = byId('commands').textContent;
    try {
      await navigator.clipboard.writeText(command);
      if (byId('commands').textContent !== command) return;
      clearTimeout(resetCopy);
      byId('copy').textContent = 'Copied';
      resetCopy = setTimeout(() => { byId('copy').textContent = 'Copy command'; }, 2500);
      byId('status').textContent = 'Command copied. Paste it in your terminal.';
    } catch {
      if (byId('commands').textContent !== command) return;
      clearTimeout(resetCopy);
      byId('copy').textContent = 'Copy manually';
      const selection = getSelection(); const range = document.createRange();
      range.selectNodeContents(byId('commands'));
      selection.removeAllRanges(); selection.addRange(range);
      byId('status').textContent = 'Clipboard unavailable. Copy the selected command manually.';
    }
  });
  fetch('catalog.json').then(response => {if (!response.ok) throw Error('Catalog unavailable'); return response.json();}).then(data => {
    if (!data.skills?.length) throw Error('Empty catalog');
    // Validate every catalogue value before it can enter a shell command.
    installation(data.skills, Object.keys(agentIds), data.repository);
    catalog = data; byId('skills').replaceChildren();
    for (const skill of data.skills) {
      const label = document.createElement('label'); const input = document.createElement('input');
      input.type = 'checkbox'; input.name = 'skill'; input.value = skill.id;
      const text = document.createElement('span');
      const name = document.createElement('strong'); name.textContent = skill.label;
      label.title = `${skill.label} v${skill.version}`;
      const description = document.createElement('small'); description.textContent = skill.description;
      text.append(name, description); label.append(input, text); byId('skills').append(label);
    }
    if (data.bundle) {
      byId('flow-title').textContent = data.bundle.label;
      byId('flow-description').textContent = data.bundle.description;
      data.bundle.steps.forEach((step, index) => {
        const item = document.createElement('li');
        const number = document.createElement('span'); number.className = 'field-step'; number.textContent = String(index + 1).padStart(2, '0');
        const title = document.createElement('strong'); title.textContent = step.title;
        const text = document.createElement('small'); text.textContent = step.text;
        const chips = document.createElement('span'); chips.className = 'flow-chips';
        for (const id of step.skills) { const chip = document.createElement('code'); chip.textContent = id; chips.append(chip); }
        item.append(number, title, text, chips); byId('flow-steps').append(item);
      });
      byId('flow-select').addEventListener('click', () => {
        const bundle = data.bundle.steps.flatMap(step => step.skills);
        for (const input of document.querySelectorAll('input[name="skill"]')) input.checked = bundle.includes(input.value);
        render();
        byId('skills').scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'nearest'});
      });
      byId('flow').hidden = false;
    }
    render();
  }).catch(() => {
    catalog = undefined; byId('skills').textContent = 'Skill list unavailable.';
    byId('install-panel').dataset.state = 'error';
    byId('where').textContent = 'Could not load the skill list. Reload this page to try again.';
    byId('copy').disabled = true; byId('install-content').hidden = true; byId('summary').hidden = true;
  });
}
