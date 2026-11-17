// Progressive enhancement: every essential record and route is server-rendered.
const toggle = document.querySelector('.menu-toggle');
const menu = document.querySelector('#primary-menu');
if (toggle && menu) {
  toggle.hidden = false;
  menu.classList.add('menu-enhanced');
  const close = () => { menu.classList.remove('is-open'); toggle.setAttribute('aria-expanded', 'false'); };
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    menu.classList.toggle('is-open', open);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') { close(); toggle.focus(); }
  });
  document.addEventListener('click', event => {
    if (!menu.contains(event.target) && !toggle.contains(event.target)) close();
  });
}
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
if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add('reveal-run'); observer.unobserve(entry.target); }
  }), { threshold: 0.08 });
  document.querySelectorAll('[data-reveal]').forEach(section => observer.observe(section));
}
if (document.querySelector('[data-site-search]')) import('./search.js').catch(() => {
  document.querySelector('#search-count').textContent = 'Interactive search unavailable. Browse all records below or use your browser’s Find command.';
});
// Keep a reader's filters, search query and section when changing language.
document.querySelectorAll('a[data-language]').forEach(anchor => {
  anchor.addEventListener('click', () => {
    const url = new URL(anchor.href);
    url.search = location.search;
    url.hash = location.hash;
    anchor.href = url.href;
  });
});
