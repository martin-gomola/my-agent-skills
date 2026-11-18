for (const block of document.querySelectorAll('pre[data-copy]')) {
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'copy';
  button.textContent = 'Copy';
  button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(block.firstChild.textContent.trim());
      button.textContent = 'Copied';
    } catch {
      const range = document.createRange();
      range.selectNodeContents(block.firstChild);
      getSelection().removeAllRanges();
      getSelection().addRange(range);
      button.textContent = 'Press ⌘C / Ctrl+C';
    }
    setTimeout(() => { button.textContent = 'Copy'; }, 2500);
  });
  block.append(button);
}
