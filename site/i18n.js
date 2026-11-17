// Translation catalogs are local, editable drafts. No browser translation service.
(() => {
  const messages = window.OSRI_MESSAGES || {};
  const language = document.documentElement.lang;
  const translate = value => {
    const source = String(value ?? '');
    const key = source.trim();
    let text = messages[key];
    if (!text) {
      const match = key.match(/^(\d+) of (\d+) shown$/);
      if (match) text = (messages['{shown} of {total} shown'] || '{shown} of {total} shown').replace('{shown}', match[1]).replace('{total}', match[2]);
      const patterns = [
        [/^(\d+) matching venues?$/, '{count} matching venues', 'count'],
        [/^(\d+) of 3 venues selected$/, '{count} of 3 venues selected', 'count'],
        [/^Compare selected venues \((\d+)\/3\)$/, 'Compare selected venues ({count}/3)', 'count'],
        [/^Source (\d+)$/, 'Source {count}', 'count'],
        [/^Compare (.+)$/, 'Compare {name}', 'name'],
        [/^Remove (.+) from comparison$/, 'Remove {name} from comparison', 'name'],
      ];
      for (const [pattern, template, variable] of patterns) {
        const match = key.match(pattern);
        if (!text && match && messages[template]) text = messages[template].replace('{' + variable + '}', match[1]);
      }
    }
    return text ? source.slice(0, source.length - source.trimStart().length) + text + source.slice(source.trimEnd().length) : source;
  };
  window.osriTranslate = translate;
  function update(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      if (node.parentElement?.closest('script,style,pre,code,kbd,samp,svg,[translate="no"],[data-language]')) return;
      const text = translate(node.data);
      if (text !== node.data) node.data = text;
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      if (node.matches('script,style,pre,code,kbd,samp,svg,[translate="no"],[data-language]')) return;
      for (const attribute of ['title', 'alt', 'placeholder', 'aria-label']) {
        if (node.hasAttribute(attribute)) node.setAttribute(attribute, translate(node.getAttribute(attribute)));
      }
      for (const child of node.childNodes) update(child);
    }
  }
  update(document.body);
  new MutationObserver(records => {
    for (const record of records) {
      if (record.type === 'characterData') update(record.target);
      else for (const node of record.addedNodes) update(node);
    }
  }).observe(document.body, { subtree: true, childList: true, characterData: true });
  window.osriLanguage = language;
})();
