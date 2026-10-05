(function(){var d=document,r=d.documentElement,b=d.getElementById('bar');
d.getElementById('tg').onclick=function(){var t=r.dataset.theme==='dark'?'light':'dark';r.dataset.theme=t;try{localStorage.setItem('theme',t)}catch(e){}this.textContent=t==='dark'?'☀️':'🌙'};
d.getElementById('tg').textContent=r.dataset.theme==='dark'?'☀️':'🌙';
d.getElementById('bg').onclick=function(){d.getElementById('links').classList.toggle('open')};
addEventListener('scroll',function(){var h=r.scrollHeight-innerHeight;b.style.transform='scaleX('+(h>0?scrollY/h:0)+')'},{passive:true});
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.05});
d.querySelectorAll('.rv').forEach(function(el,i){el.style.transitionDelay=(i%3)*60+'ms';io.observe(el)});
var co=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;co.unobserve(e.target);var n=+e.target.dataset.n,s=e.target.dataset.s||'',t0;(function f(ts){t0=t0||ts;var p=Math.min((ts-t0)/1200,1);e.target.textContent=Math.round(n*p)+s;if(p<1)requestAnimationFrame(f)})(performance.now())})});
d.querySelectorAll('[data-n]').forEach(function(el){co.observe(el)});
d.querySelectorAll('.cat,.card').forEach(function(c){c.addEventListener('pointermove',function(e){var q=c.getBoundingClientRect();c.style.setProperty('--mx',e.clientX-q.left+'px');c.style.setProperty('--my',e.clientY-q.top+'px')})});
d.querySelectorAll('.links a').forEach(function(a){a.addEventListener('click',function(){d.getElementById('links').classList.remove('open')})});
var h=d.querySelector('.hero');if(h&&matchMedia('(pointer:fine)').matches){h.addEventListener('pointermove',function(e){var x=e.clientX/innerWidth-.5,y=e.clientY/innerHeight-.5;h.querySelectorAll('.blob').forEach(function(el,i){el.style.translate=(x*40*(i+1))+'px '+(y*30*(i+1))+'px'});var o=h.querySelector('.orb');if(o)o.style.rotate=(x*6)+'deg'})}
})();
