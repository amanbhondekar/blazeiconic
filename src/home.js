// Home only: package list -> preview swap (blur + scale crossfade, as in the reference).
// Scroll reveal and the drag rail live in main.js so every page shares them.
const rows = document.querySelectorAll('.hx-row[data-index]');
const preview = document.getElementById('hxPreview');
const tag = document.getElementById('hxPreviewTag');

if (preview && rows.length) {
  // Warm the cache so swaps never flash
  for (let i = 1; i <= rows.length; i++) new Image().src = `/assets/img/prev-${i}.jpg`;

  rows.forEach((row) => {
    const activate = () => {
      if (row.classList.contains('is-active')) return;
      rows.forEach((r) => r.classList.remove('is-active'));
      row.classList.add('is-active');
      const n = Number(row.dataset.index) + 1;
      preview.classList.add('swap');
      setTimeout(() => {
        preview.src = `/assets/img/prev-${n}.jpg`;
        tag.textContent = 'Preview 0' + n;
        preview.classList.remove('swap');
      }, 350);
    };
    row.addEventListener('mouseenter', activate);
    row.addEventListener('focus', activate);
  });
}
