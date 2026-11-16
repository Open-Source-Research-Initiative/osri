// Static directory: URL state, transparent filters, and an account-free shortlist.
(()=>{
'use strict';
const root=document.getElementById('venue-directory');
if(!root)return;
const catalog=JSON.parse(document.getElementById('venue-catalog').textContent);
const $=id=>root.querySelector('#'+id);
const escapeText=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const label=s=>String(s??'unknown').replaceAll('_',' ');
const link=(u,t)=>/^https?:\/\//.test(u||'')?`<a href="${escapeText(u)}" target="_blank" rel="noopener noreferrer">${escapeText(t)}</a>`:escapeText(t);
const fields=new Map(catalog.subfields.map(s=>[s.id,s.name]));
const byId=new Map(catalog.venues.map(v=>[v.id,v]));
const views=Object.fromEntries(Object.entries(catalog.views).map(([k,ids])=>[k,new Set(ids)]));
const qualityLabels={supported:'Core standards documented',needs_verification:'Verification incomplete',concerns:'Concerns documented'};
const defaults={query:'',subfield:'',view:'documented',eligibility:'',quality:'','location-basis':'venue',region:'',country:'',sort:'name'};
let selected=[];
catalog.subfields.forEach(s=>$('subfield').add(new Option(s.name,s.id)));
const countryRegions={US:'North America',CA:'North America',MX:'North America',CR:'North America',GT:'North America',PA:'North America',CU:'North America',JM:'North America',DO:'North America',TT:'North America',BR:'South America',AR:'South America',CL:'South America',CO:'South America',PE:'South America',UY:'South America',EC:'South America',BO:'South America',PY:'South America',VE:'South America',GB:'Europe',IE:'Europe',FR:'Europe',DE:'Europe',NL:'Europe',BE:'Europe',CH:'Europe',AT:'Europe',IT:'Europe',ES:'Europe',PT:'Europe',SE:'Europe',NO:'Europe',DK:'Europe',FI:'Europe',PL:'Europe',CZ:'Europe',GR:'Europe',SK:'Europe',SI:'Europe',HR:'Europe',RS:'Europe',RO:'Europe',BG:'Europe',LT:'Europe',LV:'Europe',EE:'Europe',UA:'Europe',HU:'Europe',LU:'Europe',IS:'Europe',AL:'Europe',BA:'Europe',ME:'Europe',MK:'Europe',MD:'Europe',BY:'Europe',JP:'Asia',CN:'Asia',IN:'Asia',KR:'Asia',SG:'Asia',HK:'Asia',TW:'Asia',IL:'Asia',IR:'Asia',PK:'Asia',BD:'Asia',LK:'Asia',NP:'Asia',VN:'Asia',PH:'Asia',MY:'Asia',ID:'Asia',TH:'Asia',AU:'Oceania',NZ:'Oceania',ZA:'Africa',EG:'Africa',NG:'Africa',KE:'Africa',GH:'Africa',ET:'Africa',TZ:'Africa',MA:'Africa',TN:'Africa',UG:'Africa',DZ:'Africa',TR:['Europe','Asia'],RU:['Europe','Asia']};
function locations(v){return $('location-basis').value==='publisher'?(v.geography?.publisher_countries||[]):(v.geography?.venue_countries||[])}
function regions(v){return $('location-basis').value==='publisher'?[...new Set(locations(v).flatMap(c=>countryRegions[c.code]||[]))]:(v.geography?.venue_regions||[])}
function options(id,values){const el=$(id),old=el.value;el.replaceChildren(new Option(id==='region'?'All regions':'All countries',''));values.sort((a,b)=>a[1].localeCompare(b[1])).forEach(([value,name])=>el.add(new Option(name,value)));if([...el.options].some(o=>o.value===old))el.value=old}
function updateLocations(){$('region-label').textContent=$('location-basis').value==='publisher'?'Publisher region':'Venue region';$('country-label').textContent=$('location-basis').value==='publisher'?'Publisher country':'Venue country';options('region',[...new Set(catalog.venues.flatMap(regions))].map(x=>[x,x]));options('country',[...new Map(catalog.venues.flatMap(locations).map(c=>[c.code,c.name]))])}
function metric(v,type){return (v.metrics||[]).filter(m=>{const n=(m.name||'').toLowerCase();return type==='acceptance'?/acceptance.*rate|rate.*acceptance/.test(n):type==='jif'?/impact factor|\bjif\b/.test(n)&&!/(5.?year|five.?year)/.test(n):/citescore/.test(n)&&!n.includes('tracker')}).sort((a,b)=>{const year=x=>{const m=String(x.year??'').match(/\b(?:19|20)\d{2}\b/g);return m?Math.max(...m.map(Number)):0};return year(b)-year(a)})[0]}
function numericMetric(v,type){const m=metric(v,type);if(!m||m.value===null||m.value===undefined)return null;const raw=String(m.value).trim();if(!/^[+-]?(?:\d+(?:\.\d+)?|\.\d+)\s*%?$/.test(raw))return null;const n=Number(raw.replace('%','').trim());return Number.isFinite(n)?n:null}
function metricItem(m){return `${link(m.source_url,m.name)}: <strong>${escapeText(m.value??'Not reported')}</strong> · ${escapeText(m.year??'Year not reported')} · ${escapeText(m.population??'Population not reported')}${m.note?' · '+escapeText(m.note):''}`}
function metricHeadline(m){const period=String(m.year??'');return `${link(m.source_url,m.name)}: <strong>${escapeText(m.value??'Not reported')}</strong> · ${escapeText(/(?:19|20)\d{2}/.test(period)?period:'Year not reported')}`}
function cost(value,eligibility){return value==='none'?(eligibility==='verified_free'?'No fee':'No base fee reported; total costs not verified'):value==='charged'?'Charged': 'Not verified'}
function sources(urls){return (urls||[]).map((u,i)=>link(u,`Source ${i+1}`)).join(' · ')}
function qualityDetails(q){if(!q)return '<h3>Quality review</h3><p>Not available.</p>';const standards=q.editorial_standards||{};return `<h3>Quality review</h3><p><strong>${escapeText(qualityLabels[q.status]||'Not available')}</strong> · Checked ${escapeText(q.checked_on)}. ${escapeText(q.summary)}</p><p>Identity: ${escapeText(q.identity?.publisher||'Not reported')} · ISSNs: ${escapeText((q.identity?.issns||[]).join(', ')||'Not reported')}. ${escapeText(q.identity?.notes||'')} ${sources(q.identity?.source_urls)}</p><h3>Index and directory evidence</h3><ul>${(q.indexing||[]).map(x=>`<li><strong>${escapeText(x.name)}</strong> · ${escapeText(label(x.category))} · ${escapeText(label(x.verification))} · ${escapeText(label(x.access))}${x.coverage?' · '+escapeText(x.coverage):''}. ${escapeText(x.note||'')} ${x.registry_url?link(x.registry_url,'Registry record'):''} ${x.publisher_url?link(x.publisher_url,'Publisher claim'):''} ${sources(x.source_urls)}</li>`).join('')||'<li>No index evidence recorded.</li>'}</ul><p>Index absence is not misconduct. DOI registration and Google Scholar discovery are not selective index inclusion; PubMed is not MEDLINE.</p><h3>Peer review</h3><p>${escapeText(label(q.peer_review?.verification))} · ${escapeText(label(q.peer_review?.model))}. ${escapeText(q.peer_review?.summary||'')} ${escapeText(q.peer_review?.notes||'')} ${sources(q.peer_review?.source_urls)}</p><h3>Editorial standards</h3><ul>${Object.entries(standards).map(([name,x])=>`<li><strong>${escapeText(label(name))}</strong> · ${escapeText(label(x.status))}. ${escapeText(x.note||'')} ${(x.names||[]).map(n=>escapeText([n.name,n.role,n.affiliation].filter(Boolean).join(', '))).join('; ')} ${sources(x.source_urls)}</li>`).join('')}</ul><h3>Publication samples</h3><ul>${(q.publication_checks||[]).map(x=>`<li>${link(x.url,x.title)}${x.doi?' · DOI '+escapeText(x.doi):''}${x.published_on?' · '+escapeText(x.published_on):''}. ${escapeText(x.observations)} ${sources(x.source_urls)}</li>`).join('')||'<li>No accessible sample recorded.</li>'}</ul><h3>Specific concerns</h3><ul>${(q.concerns||[]).map(x=>`<li><strong>${escapeText(label(x.severity))}</strong>: ${escapeText(x.summary)} ${escapeText(x.rationale)} ${sources(x.evidence_urls)}</li>`).join('')||'<li>No specific concerns recorded.</li>'}</ul><h3>Evidence and limits</h3><ul>${(q.evidence||[]).map(x=>`<li>${link(x.url,label(x.source_type))} · ${escapeText(label(x.access))} · ${escapeText(x.checked_on)}: ${escapeText(x.note)}</li>`).join('')}</ul><p>${escapeText(q.audit_limits||'')}</p>`}


function note(text){$('selection-notice').textContent=text;}
function readURL(){
 const params=new URL(location.href).searchParams;
 for(const [id,value] of Object.entries(defaults))$(id).value=value;
 for(const [id,value] of Object.entries(defaults)){
  if(['region','country'].includes(id))continue;
  const target=$(id),incoming=params.get(id)??value;
  if(target.tagName!=='SELECT'||[...target.options].some(o=>o.value===incoming))target.value=incoming;
 }
 updateLocations();
 for(const id of ['region','country'])if([...$(id).options].some(o=>o.value===params.get(id)))$(id).value=params.get(id);
 $('peer').checked=params.get('peer')==='1';
 const ids=[...new Set((params.get('compare')||'').split(',').filter(Boolean))];
 selected=ids.filter(id=>byId.has(id)).slice(0,3);
 note(ids.some(id=>!byId.has(id))?'Some selected venues are unavailable in this directory and were ignored.':ids.length>3?'A comparison supports up to three venues; the first three were kept.':'');
 $('more-filters').open=['eligibility','quality','region','country'].some(id=>$(id).value)||$('peer').checked||$('location-basis').value!=='venue';
}
function writeURL(replace=false){
 const url=new URL(location.href);url.search='';
 for(const [id,value] of Object.entries(defaults))if($(id).value!==value)url.searchParams.set(id,$(id).value);
 if($('peer').checked)url.searchParams.set('peer','1');
 if(selected.length)url.searchParams.set('compare',selected.join(','));
 if(url.href!==location.href)history[replace?'replaceState':'pushState'](null,'',url);
}
function scope(v){return $('subfield').value?(v.scope_by_subfield?.[$('subfield').value]||v.scope_notes):Object.values(v.scope_by_subfield||{})[0]||v.scope_notes;}
function brief(text,n=230){const t=String(text||'');return escapeText(t.length>n?t.slice(0,n).replace(/\s+\S*$/,'')+'…':t);}
function warning(v){return (v.quality?.concerns||[]).map(c=>`<p class="warning"><strong>${escapeText(label(c.severity))} concern:</strong> ${escapeText(c.summary)} ${sources(c.evidence_urls)}</p>`).join('');}
function renderVenue(v){
 const r=v.route,a=v.ai_policy,d=a.disclosure;
 return `<article class="venue" data-id="${escapeText(v.id)}"><div class="venue-heading"><div><h2>${link(v.homepage,v.name)}</h2><div class="subject">${escapeText(v.subfields.map(id=>fields.get(id)).join(' · '))}</div></div><label class="check-label"><input type="checkbox" data-select="${escapeText(v.id)}" ${selected.includes(v.id)?'checked':''} aria-label="Compare ${escapeText(v.name)}">Compare</label></div><div class="venue-overview"><div><p class="scope">${brief(scope(v))}</p><div class="venue-meta"><p><strong>Editorial evidence:</strong> ${escapeText(qualityLabels[v.quality.status])}${v.quality.status==='needs_verification'?'. '+escapeText(v.quality.summary):''}</p><p><strong>AI use:</strong> Permitted with conditions · ${link(d.source_urls[0],'Disclosure instructions')} · ${link(a.policy_sources[0].url,'AI policy')}</p><p>${link(v.author_guidelines,'Author guidance')} · ${escapeText(label(v.review.type))}</p></div></div><div class="venue-costs ${r.eligibility==='verified_free'?'':'uncertain'}"><p><strong>Submission cost</strong>${escapeText(cost(r.submission_fee,r.eligibility))}</p><p><strong>Publication cost</strong>${escapeText(cost(r.publication_fee,r.eligibility))}</p><span>${escapeText(label(r.eligibility))}</span></div></div><p class="directory-note"><strong>Route conditions:</strong> ${brief(r.conditions,280)}</p>${warning(v)}<p class="directory-note"><strong>Reported metrics:</strong> ${['acceptance','jif','citescore'].map(t=>metric(v,t)).filter(Boolean).map(metricHeadline).join(' · ')||'Not reported'}</p><div class="evidence-panels">${[['costs','Scope and costs'],['ai','AI use and disclosure'],['quality','Editorial standards and indexing'],['sources','Geography and full sources']].map(([key,title])=>`<details data-panel="${key}" data-venue="${escapeText(v.id)}"><summary>${title}</summary><div class="detail" data-content></div></details>`).join('')}</div></article>`;
}
function evidencePanel(v,key){
 const r=v.route,a=v.ai_policy,d=a.disclosure,g=v.geography||{};
 if(key==='costs')return `<h3>Scope and contribution types</h3><p>${escapeText(scope(v))}</p><p>${escapeText(v.formats.map(label).join(', '))}</p><h3>Cost conditions</h3><p>${escapeText(r.conditions)}</p><p>Other mandatory costs: ${escapeText(r.other_mandatory_costs||'Not reported')}.</p><p>Reader access: ${escapeText(label(r.oa_status||r.model))}. A subscription route may restrict reader access independently of author costs.</p><h3>Fee evidence</h3><ul>${(r.fee_evidence||[]).map(e=>`<li>${link(e.url,'Policy source')} · ${escapeText(e.checked_on)} · ${escapeText(label(e.access))}: ${escapeText(e.note)}</li>`).join('')}</ul>`;
 if(key==='ai')return `<p>${escapeText(a.summary)}</p><h3>Disclosure · ${escapeText(label(d.status))}</h3><p>${escapeText(d.instructions)} ${sources(d.source_urls)}</p><ul>${(a.restrictions||[]).map(x=>`<li>${escapeText(x)}</li>`).join('')}</ul><h3>Applicable AI policies</h3><ul>${a.policy_sources.map(e=>`<li>${link(e.url,'AI policy')} · ${escapeText(e.note||'')} ${escapeText(e.applicability||'')}</li>`).join('')}</ul>`;
 if(key==='quality')return qualityDetails(v.quality);
 const countries=key=>(g[key]||[]).map(c=>`${link(c.source_url,c.name)} (${escapeText(c.basis)})`).join(' · ')||'Not reported';
 return `<h3>Geography and author eligibility</h3><p>Venue base: ${countries('venue_countries')}. Regions: ${escapeText((g.venue_regions||[]).join(', '))}.</p><p>Publisher base: ${countries('publisher_countries')}.</p><p>${escapeText(g.author_eligibility?.description||'Eligibility not stated')} ${sources(g.author_eligibility?.source_urls)}</p><p>Research focus: ${escapeText((g.research_focus_regions||[]).join(', '))}. ${escapeText(g.scope_notes)}</p><h3>Reported metrics</h3><ul>${v.metrics.map(m=>`<li>${metricItem(m)}</li>`).join('')||'<li>Not reported.</li>'}</ul><h3>Research provenance</h3><ul>${v.source_files.map(p=>`<li><a href="${escapeText((root.dataset.provenanceBase||'')+p)}">${escapeText(p)}</a></li>`).join('')}</ul>`;
}
function renderComparison(){
 $('shortlist-bar').hidden=$('comparison').hidden=!selected.length;
 $('shortlist-count').textContent=`${selected.length} of 3 venues selected`;
 $('comparison-summary').textContent=`Compare selected venues (${selected.length}/3)`;
 if(!selected.length){$('comparison-content').replaceChildren();$('comparison').open=false;return;}
 const rows=[
  ['Scope and article types',v=>`<p>${escapeText(scope(v))}</p><p>${escapeText(v.formats.map(label).join(', '))}</p>`],
  ['Submission cost',v=>escapeText(cost(v.route.submission_fee,v.route.eligibility))],
  ['Publication cost',v=>escapeText(cost(v.route.publication_fee,v.route.eligibility))],
  ['Cost conditions',v=>`<p>${escapeText(v.route.conditions)}</p><p>${escapeText(v.route.other_mandatory_costs)}</p>${sources(v.route.fee_evidence.map(e=>e.url))}`],
  ['AI use and disclosure',v=>`<p>${escapeText(v.ai_policy.summary)}</p><p>${escapeText(v.ai_policy.disclosure.instructions)}</p>${sources(v.ai_policy.disclosure.source_urls)}<ul>${v.ai_policy.restrictions.map(x=>`<li>${escapeText(x)}</li>`).join('')}</ul>`],
  ['Location and eligibility',v=>`<p>${escapeText((v.geography.venue_countries||[]).map(c=>c.name).join(', ')||'Venue location not reported')}</p><p>${escapeText(v.geography.author_eligibility.description)}</p>${sources(v.geography.author_eligibility.source_urls)}`],
  ['Peer review and standards',v=>`<p><strong>${escapeText(qualityLabels[v.quality.status])}</strong></p><p>${escapeText(v.quality.peer_review.summary)}</p>${warning(v)}${sources(v.quality.peer_review.source_urls)}`],
  ['Indexing evidence',v=>`<ul>${v.quality.indexing.map(i=>`<li>${escapeText(i.name)} · ${escapeText(label(i.category))} · ${escapeText(label(i.verification))}${i.coverage?' · '+escapeText(i.coverage):''} ${sources(i.source_urls)}</li>`).join('')}</ul><p>DOI registration is not selective index inclusion.</p>`],
  ['Reported metrics',v=>v.metrics.map(metricItem).join('<br>')||'Not reported'],
  ['Author guidance',v=>link(v.author_guidelines,'Read current instructions')]
 ];
 $('comparison-content').innerHTML=`<div class="comparison-scroll" role="region" aria-label="Venue comparison table; scroll horizontally on small screens" tabindex="0"><table><caption>Selected publication venues</caption><thead><tr><th scope="col">Compare</th>${selected.map(id=>{const v=byId.get(id);return `<th scope="col">${link(v.homepage,v.name)}<p><button type="button" data-remove="${escapeText(id)}" aria-label="Remove ${escapeText(v.name)} from comparison">Remove</button></p></th>`;}).join('')}</tr></thead><tbody>${rows.map(([name,render])=>`<tr><th scope="row">${name}</th>${selected.map(id=>`<td>${render(byId.get(id))}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
}
function render(save=false,replace=false){
 const query=$('query').value.toLowerCase().trim(),field=$('subfield').value,view=$('view').value;
 const status=$('eligibility').value,quality=$('quality').value,region=$('region').value,country=$('country').value;
 const venues=catalog.venues.filter(v=>views[view].has(v.id)&&(!query||JSON.stringify([v.name,v.subjects,v.scope_by_subfield,v.formats]).toLowerCase().includes(query))&&(!field||v.subfields.includes(field))&&(!status||v.route.eligibility===status)&&(!quality||v.quality.status===quality)&&(!region||regions(v).includes(region))&&(!country||locations(v).some(c=>c.code===country))&&(!$('peer').checked||v.review.type==='peer_reviewed'));
 const sort=$('sort').value;
 venues.sort((a,b)=>{if(sort!=='name'){const x=numericMetric(a,sort),y=numericMetric(b,sort);if(x===null&&y!==null)return 1;if(y===null&&x!==null)return -1;if(x!==null&&y!==null&&x!==y)return sort==='acceptance'?x-y:y-x;}return a.name.localeCompare(b.name);});
 $('result-count').textContent=`${venues.length} matching venue${venues.length===1?'':'s'}`;
 $('view-note').textContent=view==='documented'?'Verified free submission and publication, peer review, compatible AI policies, and core editorial standards documented. Each route has conditions.':view==='incomplete'?'Includes free routes with unresolved editorial checks. Their specific gaps are labeled; documented medium/high concerns remain excluded.':'All AI-compatible directory records, including unverified costs, conditional routes, and documented concerns. This view is for inspection; it is not a list of verified free options.';
 $('sort-note').textContent=sort==='name'?'Choose up to three venues to compare. Expand any evidence section for sources and conditions.':`${sort==='acceptance'?'Lower reported acceptance rate':'Higher reported metric value'} first. Missing values follow; check each source, period, and population.`;
 $('results').innerHTML=venues.length?venues.map(renderVenue).join(''):'<div class="empty"><h2>No venues match these filters</h2><p>Try another field or browsing mode, or reset the filters.</p></div>';
 renderComparison();if(save)writeURL(replace);
}
root.addEventListener('toggle',event=>{const d=event.target;if(d.matches('details[data-panel]')&&d.open&&!d.dataset.loaded){d.querySelector('[data-content]').innerHTML=evidencePanel(byId.get(d.dataset.venue),d.dataset.panel);d.dataset.loaded='true';}},true);
$('results').addEventListener('change',event=>{
 const id=event.target.dataset.select;if(!id)return;
 if(event.target.checked&&selected.length===3){event.target.checked=false;note('You can compare up to three venues. Remove one before adding another.');return;}
 selected=event.target.checked?[...selected,id]:selected.filter(x=>x!==id);note('');render(true);root.querySelector(`[data-select="${id}"]`)?.focus({preventScroll:true});
});
$('comparison-content').addEventListener('click',event=>{const b=event.target.closest('[data-remove]');if(!b)return;selected=selected.filter(id=>id!==b.dataset.remove);note('Venue removed from comparison.');render(true);$('comparison-summary').focus({preventScroll:true});});
$('show-comparison').addEventListener('click',()=>{$('comparison').open=true;$('comparison').scrollIntoView({block:'start'});$('comparison-summary').focus({preventScroll:true});});
$('clear-shortlist').addEventListener('click',()=>{selected=[];note('Shortlist cleared.');render(true);$('query').focus({preventScroll:true});});
$('filters').addEventListener('submit',e=>e.preventDefault());
for(const id of Object.keys(defaults).filter(id=>id!=='location-basis'))$(id).addEventListener(id==='query'?'input':'change',()=>render(true,id==='query'));
$('location-basis').addEventListener('change',()=>{$('region').value=$('country').value='';updateLocations();render(true);});
$('peer').addEventListener('change',()=>render(true));
$('reset-filters').addEventListener('click',()=>{for(const [id,value] of Object.entries(defaults))$(id).value=value;$('peer').checked=false;updateLocations();$('more-filters').open=false;note('Filters reset. Your comparison selection is kept.');render(true);});
window.addEventListener('popstate',()=>{readURL();render();});
const qc=catalog.summary.quality_review.status_counts;
$('coverage-counts').textContent=`Checked ${catalog.summary.checked_on}: ${catalog.venues.length} AI-compatible venues across ${catalog.subfields.length} subfields. ${catalog.summary.verified_free_peer_reviewed_before_quality} verified free peer-reviewed routes; ${views.documented.size} also have core standards documented. Quality across all records: ${qc.supported} documented, ${qc.needs_verification} incomplete, ${qc.concerns} with medium/high concerns. Counts overlap.`;
readURL();render();
})();
