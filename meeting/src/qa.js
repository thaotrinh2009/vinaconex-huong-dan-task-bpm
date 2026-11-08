const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const out = [];
  for (const [w,h,name,theme] of [[1440,900,'d','light'],[390,844,'m','light'],[1440,900,'dk','dark']]) {
    const p = await b.newPage({viewport:{width:w,height:h}, colorScheme: theme});
    const errs=[]; p.on('pageerror',e=>errs.push(e.message));
    await p.goto('file://'+__dirname+'/out/index.html'); await p.addStyleTag({content:'html{scroll-behavior:auto!important}'}); await p.waitForTimeout(800);
    const ov = await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
    out.push([name,'overflow',ov,'errs',errs.join('|')]);
    await p.screenshot({path:`qa_${name}_top.png`});
    if(name==='d'){
      await p.evaluate(()=>document.getElementById('s-flow').scrollIntoView()); await p.waitForTimeout(300); await p.screenshot({path:'qa_flow.png'});
      await p.evaluate(()=>document.getElementById('s-matrix').scrollIntoView()); await p.click('.mxr[data-role="CV"]'); await p.waitForTimeout(300); await p.screenshot({path:'qa_matrix.png'});
      await p.evaluate(()=>document.getElementById('B2').scrollIntoView()); await p.waitForTimeout(400); await p.screenshot({path:'qa_b2.png'}); await p.evaluate(()=>document.querySelectorAll('#B3 .ash')[1].scrollIntoView()); await p.evaluate(()=>scrollBy(0,-140)); await p.waitForTimeout(300); await p.screenshot({path:'qa_b2c.png'}); await p.evaluate(()=>scrollBy(0,700)); await p.waitForTimeout(300); await p.screenshot({path:'qa_b2d.png'});
      await p.evaluate(()=>window.scrollBy(0,900)); await p.waitForTimeout(300); await p.screenshot({path:'qa_b2b.png'});
      await p.evaluate(()=>document.getElementById('s-iss').scrollIntoView()); await p.fill('#isq','dat phong'); await p.waitForTimeout(300); await p.screenshot({path:'qa_iss.png'});
      out.push(['iss count', await p.textContent('#iscnt')]);
      await p.evaluate(()=>document.getElementById('s-ben').scrollIntoView()); await p.waitForTimeout(300); await p.screenshot({path:'qa_ben.png'});
      await p.click('#langB'); await p.waitForTimeout(300);
      const vi = await p.evaluate(()=>{const re=/[ăâđêôơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ]/i;let c=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){const el=n.parentElement;if(!el||el.closest('script,style'))continue;if(!el.getClientRects().length)continue;if(el.closest('svg')&&getComputedStyle(el).display==='none')continue;if(getComputedStyle(el).display==='none')continue;if(re.test(n.textContent))c.push(n.textContent.trim().slice(0,60))}return c});
      out.push(['vi visible in EN', vi.length, vi.slice(0,25)]);
      await p.evaluate(()=>document.getElementById('s-flow').scrollIntoView()); await p.waitForTimeout(300); await p.screenshot({path:'qa_flow_en.png'});
      await p.evaluate(()=>document.getElementById('B6').scrollIntoView()); await p.waitForTimeout(300); await p.screenshot({path:'qa_b6_en.png'});
    }
    if(name==='m'){ await p.evaluate(()=>document.getElementById('B4').scrollIntoView()); await p.waitForTimeout(300); await p.screenshot({path:'qa_m_b4.png'}); }
    if(name==='dk'){ await p.evaluate(()=>document.getElementById('s-flow').scrollIntoView()); await p.waitForTimeout(300); await p.screenshot({path:'qa_dk_flow.png'}); }
  }
  console.log(JSON.stringify(out,null,1)); await b.close();
})();
