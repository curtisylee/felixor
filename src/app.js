(function(){
"use strict";
var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
var root = document.documentElement;

/* ===================== hero mesh =====================
   Rendered at 1/12 scale and stretched: the browser's own smoothing does the
   gradient work, so this costs almost nothing per frame. */
var mesh = document.getElementById('mesh'), mx = mesh.getContext('2d');
var BLOBS = [
  {c:@@ACC_RGB@@,  r:.62, sx:.00023, sy:.00017, ox:0.0, oy:1.7},
  {c:@@DEEP_RGB@@, r:.55, sx:.00019, sy:.00026, ox:2.1, oy:0.4},
  {c:@@SEC_RGB@@,  r:.58, sx:.00015, sy:.00021, ox:4.0, oy:3.1},
  {c:@@ACC_RGB@@,  r:.40, sx:.00028, sy:.00013, ox:1.2, oy:5.2},
  {c:[34,38,60],   r:.75, sx:.00011, sy:.00015, ox:3.3, oy:2.2}
];
function sizeMesh(){ mesh.width = 96; mesh.height = Math.max(48, Math.round(96 * mesh.clientHeight / Math.max(mesh.clientWidth,1))); }
function drawMesh(t){
  var w = mesh.width, h = mesh.height;
  mx.globalCompositeOperation = 'source-over';
  mx.fillStyle = '#0A0B0E'; mx.fillRect(0,0,w,h);
  mx.globalCompositeOperation = 'lighter';
  for (var i=0;i<BLOBS.length;i++){
    var b = BLOBS[i];
    var x = (0.5 + 0.42*Math.sin(t*b.sx + b.ox)) * w;
    var y = (0.5 + 0.40*Math.cos(t*b.sy + b.oy)) * h;
    var rad = b.r * w * 0.62;
    var g = mx.createRadialGradient(x,y,0,x,y,rad);
    g.addColorStop(0,'rgba('+b.c[0]+','+b.c[1]+','+b.c[2]+',@@MESHA@@)');
    g.addColorStop(1,'rgba('+b.c[0]+','+b.c[1]+','+b.c[2]+',0)');
    mx.fillStyle = g; mx.beginPath(); mx.arc(x,y,rad,0,6.2832); mx.fill();
  }
}

/* ===================== story canvas =====================
   Particles in a noise-ish flow field. Each step tweens the field from
   scattered exploration toward a single coherent direction, which is the
   argument the copy beside it is making. */
var sc = document.getElementById('story-canvas'), sx = sc ? sc.getContext('2d') : null;
var PRESETS = [
  {coh:0.10, spd:0.9, mix:0.00, trail:0.16, w:1.0},
  {coh:0.42, spd:1.4, mix:0.34, trail:0.11, w:1.1},
  {coh:0.70, spd:1.0, mix:0.66, trail:0.08, w:1.3},
  {coh:0.96, spd:0.7, mix:1.00, trail:0.05, w:1.6}
];
var P = {coh:.10, spd:.9, mix:0, trail:.16, w:1.0}, Pfrom = null, Pto = null, tw0 = 0, TW = 900;
var parts = [], DPR = Math.min(devicePixelRatio||1, 2);
function sizeStory(){
  if (!sc) return;
  sc.width = sc.clientWidth*DPR; sc.height = sc.clientHeight*DPR;
  var n = Math.round(Math.min(1100, (sc.clientWidth*sc.clientHeight)/420));
  parts = [];
  for (var i=0;i<n;i++) parts.push({x:Math.random()*sc.width, y:Math.random()*sc.height, a:Math.random()*6.2832, life:Math.random()*220});
  sx.fillStyle = '#08090C'; sx.fillRect(0,0,sc.width,sc.height);
}
function setStep(i){
  if (!PRESETS[i]) return;
  Pfrom = {coh:P.coh,spd:P.spd,mix:P.mix,trail:P.trail,w:P.w}; Pto = PRESETS[i]; tw0 = performance.now();
}
function easeOut(t){ return 1 - Math.pow(1-t, 3); }
function drawStory(t){
  if (!sc || !sc.clientWidth) return;
  if (Pto){
    var k = Math.min(1,(t-tw0)/TW), e = easeOut(k);
    for (var key in Pto) P[key] = Pfrom[key] + (Pto[key]-Pfrom[key])*e;
    if (k>=1) Pto = null;
  }
  var w = sc.width, h = sc.height;
  sx.fillStyle = 'rgba(8,9,12,'+P.trail+')'; sx.fillRect(0,0,w,h);
  var target = -0.42;                       // the direction everything converges on
  var F=@@FROM_RGB@@, T=@@ACC_RGB@@;
  var r = Math.round(F[0]+(T[0]-F[0])*P.mix), g = Math.round(F[1]+(T[1]-F[1])*P.mix), b = Math.round(F[2]+(T[2]-F[2])*P.mix);
  sx.beginPath();
  for (var i=0;i<parts.length;i++){
    var p = parts[i];
    var field = Math.sin(p.x*0.0035/DPR + t*0.00016) + Math.cos(p.y*0.0042/DPR - t*0.00012);
    var ang = field*1.6*(1-P.coh) + target*P.coh + (1-P.coh)*Math.sin(p.a)*0.6;
    var sp = (1.1 + P.spd*1.9)*DPR;
    var nx = p.x + Math.cos(ang)*sp, ny = p.y + Math.sin(ang)*sp;
    sx.moveTo(p.x,p.y); sx.lineTo(nx,ny);
    p.x = nx; p.y = ny; p.life--;
    if (p.life<0 || p.x<-20 || p.x>w+20 || p.y<-20 || p.y>h+20){
      p.x = Math.random()*w; p.y = Math.random()*h; p.a = Math.random()*6.2832; p.life = 140+Math.random()*220;
    }
  }
  sx.strokeStyle = 'rgba('+r+','+g+','+b+',0.10)';
  sx.lineWidth = P.w*3.2*DPR; sx.stroke();
  sx.strokeStyle = 'rgba('+r+','+g+','+b+',0.85)';
  sx.lineWidth = P.w*DPR; sx.stroke();
}

/* ===================== frame loop ===================== */
var heroVis = false, storyVis = false, raf = 0;
function frame(t){
  if (heroVis) drawMesh(t);
  if (storyVis) drawStory(t);
  raf = (heroVis||storyVis) ? requestAnimationFrame(frame) : 0;
}
function kick(){ if (!raf && (heroVis||storyVis)) raf = requestAnimationFrame(frame); }

/* ===================== reveals ===================== */
var revealIO = new IntersectionObserver(function(es){
  es.forEach(function(e){ if (e.isIntersecting){ e.target.classList.add('in'); revealIO.unobserve(e.target); } });
}, {rootMargin:'0px 0px -10% 0px', threshold:.1});
function observeReveals(scope){
  (scope||document).querySelectorAll('.rise:not(.in),.pop:not(.in)').forEach(function(el){
    if (reduce) el.classList.add('in'); else revealIO.observe(el);
  });
}

/* ===================== ground colour ===================== */
var ground = document.querySelector('.ground');
var groundIO = new IntersectionObserver(function(es){
  es.forEach(function(e){ if (e.isIntersecting) ground.style.background = e.target.dataset.ground; });
}, {rootMargin:'-40% 0px -40% 0px'});
document.querySelectorAll('[data-ground]').forEach(function(el){ groundIO.observe(el); });

/* ===================== scrollytelling =====================
   One observer per step, with a band at the vertical centre of the viewport.
   Because IntersectionObserver reports both directions, scrolling back up
   walks the sequence backwards for free. */
var steps = [].slice.call(document.querySelectorAll('.step'));
var labs  = [].slice.call(document.querySelectorAll('.vis-label .lab b'));
var bar   = document.querySelector('.bar span');
var current = -1;
function activate(i){
  if (i === current) return;
  current = i;
  steps.forEach(function(s,n){ s.classList.toggle('on', n===i); });
  labs.forEach(function(l,n){ l.classList.toggle('on', n===i); });
  if (bar) bar.style.transform = 'scaleX(' + ((i+1)/steps.length) + ')';
  setStep(i);
}
if (steps.length){
  var stepIO = new IntersectionObserver(function(es){
    es.forEach(function(e){ if (e.isIntersecting) activate(steps.indexOf(e.target)); });
  }, {rootMargin:'-48% 0px -48% 0px', threshold:0});
  steps.forEach(function(s){ stepIO.observe(s); });
  new IntersectionObserver(function(es){
    storyVis = es[0].isIntersecting; kick();
  },{threshold:0}).observe(document.querySelector('.story'));
}
if (mesh){
  new IntersectionObserver(function(es){ heroVis = es[0].isIntersecting; kick(); },{threshold:0}).observe(mesh);
}

/* ===================== nav ===================== */
var nav = document.getElementById('nav');
var sentinel = document.createElement('div');
sentinel.setAttribute('aria-hidden','true');
sentinel.style.cssText = 'position:absolute;top:0;left:0;width:1px;height:80px;pointer-events:none';
document.body.prepend(sentinel);
new IntersectionObserver(function(es){ nav.classList.toggle('stuck', !es[0].isIntersecting); },{threshold:0}).observe(sentinel);

var pill = document.querySelector('.navpill');
function movePill(){
  var a = document.querySelector('.navlinks a[aria-current="page"]');
  if (!a || !pill){ if (pill) pill.classList.remove('on'); return; }
  pill.style.width = a.offsetWidth + 'px';
  pill.style.transform = 'translateX(' + a.offsetLeft + 'px)';
  pill.classList.add('on');
}

/* ===================== router ===================== */
var TITLES = {'':'Felixor', 'portfolio':'Portfolio | Felixor', 'about':'About | Felixor'};
function routeKey(){
  var h = location.hash.replace(/^#\/?/, '').replace(/\/$/,'');
  return h || '';
}
function pageFor(key){
  return document.getElementById('page-' + (key ? key.replace('/','-') : 'home')) || document.getElementById('page-home');
}
function go(){
  var key = routeKey(), next = pageFor(key), cur = document.querySelector('.page.active');
  document.querySelectorAll('.navlinks a').forEach(function(a){
    var t = a.getAttribute('href').replace(/^#\/?/,'').replace(/\/$/,'');
    if (t === key || (t === '' && key === '')) a.setAttribute('aria-current','page');
    else a.removeAttribute('aria-current');
  });
  // product pages keep the Portfolio tab lit
  if (key.indexOf('product/') === 0){
    var pa = document.querySelector('.navlinks a[href="#/portfolio"]');
    if (pa) pa.setAttribute('aria-current','page');
  }
  movePill();
  document.title = TITLES[key] || (next && next.dataset.title) || 'Felixor';

  if (cur === next){ return; }
  function swap(){
    if (cur){ cur.classList.remove('active','entering','leaving'); }
    next.classList.add('active');
    if (!reduce){
      next.classList.add('entering');
      setTimeout(function(){ next.classList.remove('entering'); }, 520);
    }
    window.scrollTo(0,0);
    observeReveals(next);
    current = -1;
    if (next.id === 'page-home' && steps.length){ activate(0); }
    requestAnimationFrame(function(){ sizeStory(); sizeMesh(); kick(); movePill(); });
  }
  if (cur && !reduce){
    cur.classList.add('leaving');
    setTimeout(swap, 180);
  } else swap();
}
addEventListener('hashchange', go);

/* ===================== boot ===================== */
function boot(){
  sizeMesh(); sizeStory();
  root.classList.add('ready');
  requestAnimationFrame(function(){ requestAnimationFrame(function(){ root.classList.add('lit'); }); });
  go();
  observeReveals(document);
  if (reduce){ drawMesh(0); if (sc){ setStep(3); P = {coh:.96,spd:.7,mix:1,trail:.05,w:1.6}; for(var i=0;i<160;i++) drawStory(i*16); } }
  kick();
}
var rz; addEventListener('resize', function(){
  clearTimeout(rz); rz = setTimeout(function(){ sizeMesh(); sizeStory(); movePill(); }, 180);
});
if (document.readyState === 'loading') addEventListener('DOMContentLoaded', boot); else boot();
})();
