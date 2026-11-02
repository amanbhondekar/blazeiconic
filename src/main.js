// Scroll reveal (reference: clip-path wipe once, when 15% is in view)
(() => {
  const els = document.querySelectorAll('.reveal');
  if (!els.length) return;
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.15 });
  els.forEach((el) => io.observe(el));
})();

// Drag-to-scroll rails
document.querySelectorAll('.hx-rail').forEach((rail) => {
  let down = false, startX = 0, startLeft = 0, moved = false;
  rail.addEventListener('pointerdown', (e) => { down = true; moved = false; startX = e.clientX; startLeft = rail.scrollLeft; });
  window.addEventListener('pointerup', () => { down = false; rail.classList.remove('dragging'); });
  window.addEventListener('pointermove', (e) => {
    if (!down) return;
    const dx = e.clientX - startX;
    if (Math.abs(dx) > 3) { moved = true; rail.classList.add('dragging'); }
    rail.scrollLeft = startLeft - dx;
  });
  rail.addEventListener('click', (e) => { if (moved) e.preventDefault(); }, true);
});

// Mobile menu
(() => {
  const btn = document.querySelector('.menu-btn');
  const nav = document.getElementById('site-nav');
  if (!btn || !nav) return;

  const set = (open) => {
    document.body.classList.toggle('menu-open', open);
    btn.setAttribute('aria-expanded', String(open));
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  };

  btn.addEventListener('click', () => set(!document.body.classList.contains('menu-open')));
  nav.addEventListener('click', (e) => { if (e.target.closest('a')) set(false); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') set(false); });
  window.matchMedia('(min-width: 1100px)').addEventListener('change', (m) => { if (m.matches) set(false); });
})();
