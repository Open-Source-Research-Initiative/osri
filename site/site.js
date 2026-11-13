document.querySelectorAll('[data-filter]').forEach(section => {
  const form = section.querySelector('form');
  const search = form.querySelector('[name="search"]');
  const area = form.querySelector('[name="area"]');
  const items = [...section.querySelectorAll('[data-filter-item]')];
  const count = section.querySelector('.filter-count');
  const empty = section.querySelector('.filter-empty');
  const normalize = value => value.normalize('NFKC').toLocaleLowerCase();
  const update = () => {
    const words = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    let shown = 0;
    items.forEach(item => {
      const text = normalize(item.dataset.search || item.textContent);
      const areas = (item.dataset.area || '').split(';').map(value => value.trim());
      const match = words.every(word => text.includes(word)) && (!area || !area.value || areas.includes(area.value));
      item.hidden = !match;
      if (match) shown += 1;
    });
    count.textContent = `${shown} of ${items.length} shown`;
    if (empty) empty.hidden = shown > 0;
  };
  form.addEventListener('submit', event => event.preventDefault());
  form.addEventListener('input', update);
  form.addEventListener('change', update);
  update();
});
