
(()=>{
 const header=document.querySelector('.global-header');if(!header)return;
 const toggle=header.querySelector('.global-menu-toggle');
 const nav=header.querySelector('.global-nav');
 const caseMenu=header.querySelector('.global-case-menu');
 const caseTrigger=header.querySelector('.global-case-trigger');
 const lock=v=>{document.documentElement.classList.toggle('global-nav-open',v);document.body.classList.toggle('global-nav-open',v)};
 const closeCases=()=>{if(!caseMenu||!caseTrigger)return;caseMenu.classList.remove('is-open');caseTrigger.setAttribute('aria-expanded','false')};
 const closeNav=()=>{if(!toggle||!nav)return;nav.classList.remove('is-open');toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label','Open navigation');lock(false);closeCases()};
 if(toggle&&nav)toggle.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';nav.classList.toggle('is-open',open);toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Close navigation':'Open navigation');lock(open&&matchMedia('(max-width:900px)').matches);if(!open)closeCases()});
 if(caseMenu&&caseTrigger)caseTrigger.addEventListener('click',e=>{e.stopPropagation();const open=caseTrigger.getAttribute('aria-expanded')!=='true';caseMenu.classList.toggle('is-open',open);caseTrigger.setAttribute('aria-expanded',String(open))});
 document.addEventListener('click',e=>{if(caseMenu&&!caseMenu.contains(e.target))closeCases()});
 document.addEventListener('keydown',e=>{if(e.key!=='Escape')return;const wasOpen=nav&&nav.classList.contains('is-open');closeCases();if(wasOpen){closeNav();toggle?.focus()}else caseTrigger?.focus()});
 header.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{if(matchMedia('(max-width:900px)').matches)closeNav()}));
 addEventListener('resize',()=>{if(!matchMedia('(max-width:900px)').matches)closeNav()});
 document.querySelectorAll('[data-global-year]').forEach(el=>el.textContent=new Date().getFullYear());
})();
