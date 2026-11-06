const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs');
(async () => {
 const browser=await chromium.launch({headless:true});
 fs.mkdirSync('docs/design-review',{recursive:true});
 const report=[];
 for (const [width,height] of [[720,450],[1440,900],[1920,1080],[1280,800],[1024,768],[768,1024],[390,844],[320,740]]) {
  const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)errors.push(r.url()+': '+r.status())});
  await page.addInitScript(()=>{window.reviewCLS=0;new PerformanceObserver(list=>{for(const entry of list.getEntries())if(!entry.hadRecentInput)window.reviewCLS+=entry.value}).observe({type:'layout-shift',buffered:true});});
  await page.goto('http://127.0.0.1:4175/',{waitUntil:'networkidle'});await page.evaluate(()=>document.fonts.ready);
  await page.addScriptTag({path:require.resolve(process.env.AXE_MODULE || 'axe-core')});
  const axe=await page.evaluate(async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return {violations:r.violations,incomplete:r.incomplete.map(x=>({id:x.id,targets:x.nodes.map(n=>n.target)}))};});
  if(axe.violations.length)throw Error(JSON.stringify({width,axe},null,2));
  const data=await page.evaluate(()=>({cls:window.reviewCLS,resourceBytes:performance.getEntriesByType('resource').reduce((n,r)=>n+r.encodedBodySize,0),overflow:document.documentElement.scrollWidth>innerWidth,hero:document.querySelector('.hero').getBoundingClientRect().height,image:document.querySelector('.hero img').currentSrc,fonts:document.fonts.check('16px "DM Sans"')&&document.fonts.check('16px "Libre Caslon Display"'),h1:document.querySelector('h1').textContent,services:document.querySelectorAll('.service').length,mailLinks:[...document.querySelectorAll('a[href^="mailto:"]')].map(a=>a.href)}));
  if(data.overflow||!data.fonts||errors.length||data.cls>0.1||data.services!==6||data.mailLinks.length!==5||data.mailLinks.some(h=>h!=='mailto:jay@tyrus.com'))throw Error(JSON.stringify({width,data,errors}));
  if(width===1440||width===390){await page.screenshot({path:`docs/design-review/${width===1440?'desktop':'mobile'}-full.png`,fullPage:true});await page.screenshot({path:`docs/design-review/${width===1440?'desktop':'mobile'}-hero.png`});}
  if(width<=760){
   const toggle=page.getByRole('button',{name:'Menu'});await toggle.click();if(await toggle.getAttribute('aria-expanded')!=='true')throw Error('Menu open failed');
   await page.keyboard.press('Escape');if(await toggle.getAttribute('aria-expanded')!=='false')throw Error('Escape failed');
   if(!await toggle.evaluate(e=>document.activeElement===e))throw Error('Focus restore failed');
   await toggle.click();await page.locator('#navigation a[href="#expertise"]').click();if(await toggle.getAttribute('aria-expanded')!=='false')throw Error('Anchor close failed');
   await page.waitForTimeout(500);
  }
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.evaluate(()=>document.querySelector('#contact').scrollIntoView());
  await page.waitForTimeout(100);
  if(!await page.locator('.header').evaluate(e=>e.classList.contains('is-scrolled')))throw Error('Scrolled header surface failed');
  if(!await page.locator('#contact').evaluate(e=>e.getBoundingClientRect().top>=document.querySelector('.header').getBoundingClientRect().bottom))throw Error('Sticky navigation obscures contact');
  report.push({width,height,...data,errors,axe});await page.close();
 }
 const page=await browser.newPage({viewport:{width:1440,height:900},reducedMotion:'reduce'});await page.goto('http://127.0.0.1:4175/');
 await page.keyboard.press('Tab');if(!await page.locator('.skip-link').evaluate(e=>e===document.activeElement))throw Error('Skip link focus failed');
 await page.keyboard.press('Enter');if(!await page.locator('main').evaluate(e=>e===document.activeElement))throw Error('Skip target focus failed');
 if(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior)!=='auto')throw Error('Reduced motion failed');
 await page.close();
 fs.writeFileSync('docs/design-review/browser-results.json',JSON.stringify({viewports:report,keyboard:'Skip link; mobile menu open/close; Escape and focus restore passed',reducedMotion:'passed'},null,2));
 await browser.close();console.log('PASS: 8 viewports, image/font loading, overflow, mobile menu, keyboard and reduced motion.');
})();
