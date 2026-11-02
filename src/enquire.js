// One enquiry flow: "What can we help you with?" picks the fields that follow.
// Without JavaScript every group stays visible, so the form still works.
(() => {
  const form = document.getElementById('enquiryForm');
  if (!form) return;
  const radios = form.querySelectorAll('input[name="type"]');
  const groups = form.querySelectorAll('[data-type]');
  const rest = form.querySelector('[data-rest]');

  const show = (type) => {
    groups.forEach((g) => {
      const on = g.dataset.type === type;
      g.classList.toggle('on', on);
      g.querySelectorAll('input, select, textarea').forEach((f) => { f.disabled = !on; });
    });
    if (rest) rest.classList.toggle('on', Boolean(type));
  };

  radios.forEach((r) => r.addEventListener('change', () => show(r.value)));

  const params = new URLSearchParams(location.search);
  const want = params.get('type');
  const match = [...radios].find((r) => r.value === want);
  if (match) match.checked = true;
  const talent = params.get('talent');
  const talentField = form.querySelector('[name="talent"]');
  if (talent && talentField) talentField.value = talent;

  const checked = [...radios].find((r) => r.checked);
  show(checked ? checked.value : '');
})();
