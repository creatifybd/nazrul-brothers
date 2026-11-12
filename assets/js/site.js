
(function(){
 document.documentElement.classList.add('js-ready');
 document.querySelectorAll('[data-current-year]').forEach(el=>el.textContent=String(new Date().getFullYear()));
 const menu=document.querySelector('[data-menu-button]'),nav=document.querySelector('[data-nav]');
 if(menu && nav){
   const setOpen=open=>{nav.classList.toggle('open',open);menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'Close navigation':'Open navigation')};
   menu.addEventListener('click',()=>setOpen(menu.getAttribute('aria-expanded')!=='true'));
   nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setOpen(false)));
   document.addEventListener('keydown',e=>{if(e.key==='Escape')setOpen(false)});
   document.addEventListener('click',e=>{if(!menu.contains(e.target)&&!nav.contains(e.target))setOpen(false)});
 }
 const path=location.pathname.replace(/\/?$/,'/')||'/';
 document.querySelectorAll('[data-nav-link]').forEach(a=>{if(new URL(a.href).pathname===path)a.setAttribute('aria-current','page')});
 if('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches){
   document.body.classList.add('js-reveal');
   const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target)}}),{threshold:.06,rootMargin:'0px 0px 55px 0px'});
   document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
 }
})();
