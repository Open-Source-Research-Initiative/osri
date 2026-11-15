const form = document.querySelector('.search-form');
const query = form.elements.q;
const type = form.elements.type;
const results = document.querySelector('#search-results');
const count = document.querySelector('#search-count');
const empty = document.querySelector('#search-empty');
const normalize = text => text.normalize('NFKC').toLocaleLowerCase();
const response = await fetch('/search-index.json');
if (!response.ok) throw new Error('Search index unavailable');
const records = await response.json();
function readURL() {
  const params = new URLSearchParams(location.search);
  query.value = params.get('q') || '';
  type.value = params.get('type') || '';
}
function update(save = true) {
  const words = normalize(query.value.trim()).split(/\s+/).filter(Boolean);
  const matches = records.filter(row => (!type.value || row.type === type.value) && words.every(word => normalize(row.title + ' ' + row.text).includes(word)));
  matches.sort((a, b) => Number(words.every(word => normalize(b.title).includes(word))) - Number(words.every(word => normalize(a.title).includes(word))));
  const fragment = document.createDocumentFragment();
  matches.forEach(row => {
    const article = document.createElement('article');
    const label = document.createElement('p'); label.className = 'eyebrow'; label.textContent = row.type;
    const heading = document.createElement('h2');
    const anchor = document.createElement('a'); anchor.href = row.url; anchor.textContent = row.title; heading.append(anchor);
    const snippet = document.createElement('p');
    const content = row.text;
    const firstMatch = words.length ? normalize(content).indexOf(words[0]) : 0;
    const start = Math.max(0, firstMatch - 60);
    snippet.textContent = (start ? '…' : '') + content.slice(start, start + 220) + (content.length > start + 220 ? '…' : '');
    article.append(label, heading, snippet); fragment.append(article);
  });
  results.replaceChildren(fragment);
  count.textContent = `${matches.length} ${matches.length === 1 ? 'result' : 'results'}${type.value ? ' · ' + type.options[type.selectedIndex].text : ' · all content'}`;
  empty.hidden = matches.length > 0;
  if (save) {
    const params = new URLSearchParams();
    if (query.value.trim()) params.set('q', query.value.trim());
    if (type.value) params.set('type', type.value);
    history.replaceState(null, '', '/search/' + (params.size ? '?' + params.toString() : ''));
  }
}
form.addEventListener('submit', event => { event.preventDefault(); update(); });
form.addEventListener('input', () => update());
form.addEventListener('change', () => update());
form.addEventListener('reset', () => { query.value = ''; type.value = ''; update(); query.focus(); });
window.addEventListener('popstate', () => { readURL(); update(false); });
readURL(); update(false);
