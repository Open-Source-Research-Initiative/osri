const {chromium}=require(process.env.OSRI_PLAYWRIGHT_MODULE),fs=require('fs'),path=require('path'),assert=require('assert/strict');
const base=(process.env.OSRI_SITE_URL||'http://127.0.0.1:8798').replace(/\/$/,''),output=process.env.OSRI_QA_OUTPUT;
assert(output);fs.mkdirSync(output,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.OSRI_CHROMIUM});
 const page=await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce'}),errors=[];page.setDefaultTimeout(15000);
 page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 const identity=async route=>{const r=await page.goto(base+route);assert.equal(r.status(),200);assert.equal(await page.locator('main').count(),1);assert.equal(await page.locator('h1').count(),1);assert((await page.title()).length>8);assert((await page.locator('main').innerText()).length>100);assert.equal(await page.locator('vite-error-overlay,nextjs-portal').count(),0);};
 await identity('/venues/');assert.equal(await page.locator('.venue').count(),57);
 const nav=page.getByRole('navigation',{name:'Directory help'});assert.equal(await nav.getByRole('link').count(),4);
 assert.match(await nav.getByRole('link',{name:/Report a source/}).getAttribute('href'),/template=venue-evidence.yml/);
 assert.match(await nav.getByRole('link',{name:/Share your experience/}).getAttribute('href'),/template=directory-use.yml/);
 await page.screenshot({path:path.join(output,'directory-desktop.png')});
 await nav.getByRole('link',{name:'90-second walkthrough'}).click();
 assert(new URL(page.url()).pathname==='/guides/docs/venue-directory-demo/');
 const video=page.locator('video');await video.evaluate(v=>v.play());await page.waitForFunction(()=>document.querySelector('video').currentTime>0.3);
 const duration=await video.evaluate(v=>v.duration);assert(duration>88&&duration<92);await video.evaluate(v=>{v.pause();v.currentTime=45;});
 await page.waitForFunction(()=>{const v=document.querySelector('video');return !v.seeking&&v.readyState>=2&&v.currentTime>44;});
 const frame=await video.evaluate(v=>{const c=document.createElement('canvas');c.width=160;c.height=100;const x=c.getContext('2d');x.drawImage(v,0,0,160,100);const d=x.getImageData(0,0,160,100).data;let dark=0;for(let i=0;i<d.length;i+=4)if(d[i]+d[i+1]+d[i+2]<400)dark++;return dark;});assert(frame>200,'Decoded video frame must contain visible content');
 assert.equal(await video.evaluate(v=>v.error),null);assert.equal(await video.locator('track').count(),1);
 assert(await page.getByRole('heading',{name:/Check author costs separately/}).isVisible());
 const vtt=await page.request.get(base+'/assets/demos/venue-directory-demo.vtt');assert.equal(vtt.status(),200);assert((await vtt.text()).startsWith('WEBVTT'));
 await page.screenshot({path:path.join(output,'demo-desktop.png')});
 await identity('/contribute/');const panel=page.locator('#venue-tasks');assert(await panel.isVisible());
 assert.match(await panel.innerText(),/No code or installation/);
 await panel.getByRole('link',{name:'Choose a starter task',exact:true}).click();
 assert(new URL(page.url()).pathname==='/guides/community/venue-starter-tasks/');
 for(let n=5;n<=10;n++)assert.equal(await page.locator(`main a[href="https://github.com/Open-Source-Research-Initiative/free-publication-directory/issues/${n}"]`).count(),1);
 await identity('/venues/?subfield=public-health');assert.equal(await page.locator('.venue').count(),6);
 await page.selectOption('#subfield','education-learning-sciences');assert.equal(await page.locator('.venue').count(),6);
 for(let i=0;i<3;i++)await page.locator('.venue').nth(i).locator('[data-select]').check();
 await page.click('#show-comparison');assert(await page.getByRole('table').isVisible());const shared=page.url();
 await page.reload();assert.equal(page.url(),shared);assert.equal(await page.locator('[data-select]:checked').count(),3);
 for(const [name,width,height] of [['desktop',1440,1000],['mobile',390,844]]){
  await page.setViewportSize({width,height});
  for(const route of ['/venues/','/contribute/','/guides/docs/venue-directory-demo/','/guides/community/venue-starter-tasks/']){
   await identity(route);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),route+' overflow');
  }
  await page.goto(base+'/contribute/');await page.screenshot({path:path.join(output,'contribute-'+name+'.png')});
 }
 await page.getByRole('button',{name:/Menu/}).click();assert.equal(await page.getByRole('button',{name:/Menu/}).getAttribute('aria-expanded'),'true');
 assert.deepEqual(errors,[]);
 const report={status:'pass',base,viewports:['1440x1000','390x844'],browser:'Playwright; Browser plugin not available',flow:'directory -> walkthrough playback -> starter tasks and feedback links',video_duration_seconds:duration,checks:{page_identity:'pass',meaningful_content:'pass',no_framework_overlay:'pass',console_health:'pass',screenshots:'pass',interaction_proof:'pass'},details:['57 default venues','two field links each restore six results','compare three and restore shortlist URL','all six issue links','video plays and seeks, optional captions load','direct evidence and use-report links','desktop/mobile layout','mobile navigation'],limits:'Chromium only; no test issue submitted; no external human usability trial',errors};
 fs.writeFileSync(path.join(output,'browser-check.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
