const button = document.getElementById('copy-snippet');
const snippet = document.getElementById('snippet');
const status = document.getElementById('copy-status');
let reset;
button.addEventListener('click', async () => {
  clearTimeout(reset);
  try {
    await navigator.clipboard.writeText(snippet.textContent);
    button.textContent = 'Copied';
    status.textContent = 'Copied. Paste it into AGENTS.md or CLAUDE.md.';
    reset = setTimeout(() => { button.textContent = 'Copy for AGENTS.md'; }, 2500);
  } catch {
    button.textContent = 'Copy manually';
    const range = document.createRange();
    range.selectNodeContents(snippet);
    getSelection().removeAllRanges();
    getSelection().addRange(range);
    status.textContent = 'Clipboard unavailable. The text is selected; copy it manually.';
  }
});
