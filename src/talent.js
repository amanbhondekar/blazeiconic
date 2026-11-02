// Talent directory: filter the roster by category. Only categories the roster supports are offered.
(() => {
  const grid = document.getElementById('talentGrid');
  if (!grid) return;
  const chips = document.querySelectorAll('.hx-chip[data-filter]');
  const cards = grid.querySelectorAll('.hx-gcard');
  const empty = document.getElementById('talentEmpty');

  const apply = (key) => {
    let shown = 0;
    cards.forEach((c) => {
      const on = key === 'all' || c.dataset.cats.split(' ').includes(key);
      c.hidden = !on;
      if (on) shown++;
    });
    chips.forEach((chip) => {
      const on = chip.dataset.filter === key;
      chip.classList.toggle('is-on', on);
      chip.setAttribute('aria-pressed', String(on));
    });
    if (empty) empty.hidden = shown > 0;
  };

  chips.forEach((chip) => chip.addEventListener('click', (e) => {
    e.preventDefault();
    apply(chip.dataset.filter);
    history.replaceState(null, '', chip.dataset.filter === 'all' ? location.pathname : '#' + chip.dataset.filter);
  }));

  const fromHash = () => {
    const key = location.hash.slice(1);
    apply([...chips].some((c) => c.dataset.filter === key) ? key : 'all');
  };
  window.addEventListener('hashchange', fromHash);
  fromHash();
})();
