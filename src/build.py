import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ROOT = _os.path.dirname(_HERE)
def _s(p): return _os.path.join(_HERE, p)
def _r(p): return _os.path.join(_ROOT, p)
import json, sys
import sys as _sys; _sys.path.insert(0, _HERE)
from data import PRODUCTS, STEPS, CAREER
from palettes import PALETTES, rgb

PAL_NAME = sys.argv[1] if len(sys.argv)>1 else "iris"
PAL = PALETTES[PAL_NAME]
A, S, D = rgb(PAL["accent"]), rgb(PAL["sec"]), rgb(PAL["deep"])
from palettes import lum as _lum
_acc_lum = _lum(PAL["accent"])
FIELD_FROM = tuple(min(255, int(c*0.62)+34) for c in S)   # muted start for the flow field
SUBS = {
 "@@ACCENT@@": PAL["accent"], "@@A2@@": PAL["a2"], "@@BTN@@": PAL["btn_bg"], "@@BTNFG@@": PAL["btn"],
 "@@SEC@@": PAL["sec"],
 "@@DIM@@":   "rgba(%d,%d,%d,.14)" % A,
 "@@RING@@":  "rgba(%d,%d,%d,.38)" % A,
 "@@FAINT@@": "rgba(%d,%d,%d,.02)" % A,
 "@@ACC_RGB@@":  "[%d,%d,%d]" % A,
 "@@SEC_RGB@@":  "[%d,%d,%d]" % S,
 "@@DEEP_RGB@@": "[%d,%d,%d]" % D,
 "@@FROM_RGB@@": "[%d,%d,%d]" % FIELD_FROM,
 # darker accents need more bloom to read against near-black
 "@@MESHA@@": "%.2f" % (0.46 if _acc_lum > 0.30 else 0.78),
}
def swap(t):
    for k,v in SUBS.items(): t = t.replace(k, v)
    return t

fonts = json.load(open(_s("fonts.json")))
art   = json.load(open(_s("art.json")))
css   = swap(open(_s("style.css")).read())
js    = swap(open(_s("app.js")).read())

AR  = '<svg viewBox="0 0 256 256" aria-hidden="true" focusable="false"><path d="M200,64V168a8,8,0,0,1-16,0V83.31L69.66,197.66a8,8,0,0,1-11.32-11.32L172.69,72H88a8,8,0,0,1,0-16H192A8,8,0,0,1,200,64Z"/></svg>'
ARR = '<svg viewBox="0 0 256 256" aria-hidden="true" focusable="false"><path d="M221.66,133.66l-72,72a8,8,0,0,1-11.32-11.32L196.69,136H40a8,8,0,0,1,0-16H196.69L138.34,61.66a8,8,0,0,1,11.32-11.32l72,72A8,8,0,0,1,221.66,133.66Z"/></svg>'

HEAD = "We don't bolt AI on. We build from it."
words = "".join('<span class="w"><span style="transition-delay:%dms">%s</span></span>%s'
                % (60+i*52, w, " " if i < len(HEAD.split())-1 else "")
                for i,w in enumerate(HEAD.split()))

CAPS = ["Applied research","Product design","Model evaluation","Interface engineering",
        "Retrieval systems","Agent architecture","Rollout and adoption","Zero to one"]
track = "".join("<span>%s</span>" % c for c in CAPS)

# ---------- home ----------
steps_html = "".join(
  '<article class="step"><div class="step-n">%02d</div><h3 class="h3">%s</h3><p>%s</p></article>'
  % (i+1, s["t"], s["b"]) for i,s in enumerate(STEPS))
labs_html = "".join('<b%s>%s</b>' % (' class="on"' if i==0 else '', s["t"].rstrip('.')) for i,s in enumerate(STEPS))

def card(p):
    return ('<a class="card pop" href="#/product/%s">'
            '<div class="card-art"><div class="art" style="--art:var(--art-%s)" role="img" aria-label="Generative artwork for %s"></div></div>'
            '<div class="card-body"><div class="card-top"><h3 class="h3">%s</h3>'
            '<span class="chip chip-dev">%s</span></div>'
            '<p>%s</p><span class="go">View product %s</span></div></a>'
            ) % (p["slug"], p["art"], p["name"], p["name"], p["status"], p["tag"], AR)

home = """
<section class="hero" data-ground="#0A0B0E">
  <canvas id="mesh" aria-hidden="true"></canvas>
  <div class="wrap">
    <h1 class="display">%(words)s</h1>
    <div class="rule" aria-hidden="true"></div>
    <p class="lead hero-lag">Felixor is an AI product studio. We design, build, and ship products where the intelligence is the foundation, not a feature.</p>
    <div class="hero-actions hero-lag">
      <a class="btn btn-primary btn-lg" href="#/portfolio">See what we are building %(ar)s</a>
      <a class="btn btn-ghost btn-lg" href="#/about">About the studio</a>
    </div>
  </div>
</section>

<div class="strip" aria-hidden="true"><div class="track">%(track)s%(track)s</div></div>

<section class="section" data-ground="#0B0D12">
  <div class="wrap">
    <h2 class="h2 rise" style="max-width:17ch">Studios ship products. Consultancies ship recommendations.</h2>
    <p class="body rise d1" style="margin-top:1.75rem">We are the first kind. Felixor holds equity in what it builds, carries the roadmap, and lives with the consequences of its own design decisions. Some products we build alone. Some we build with a partner who brings the domain and the distribution.</p>
    <p class="body rise d2">What does not change is the starting point. We only build where a model can now do something it genuinely could not do three years ago, and where that capability removes work rather than adding a panel to it.</p>
  </div>
</section>

<section class="story section-b" data-ground="#0C0A10">
  <div class="wrap story-grid">
    <div class="steps">%(steps)s</div>
    <div class="sticky">
      <div class="vis-frame">
        <canvas id="story-canvas" aria-hidden="true"></canvas>
        <div class="vis-label"><span class="lab">%(labs)s</span><div class="bar"><span></span></div></div>
      </div>
    </div>
  </div>
</section>

<section class="section section-b" data-ground="#0A0B0E">
  <div class="wrap">
    <h2 class="h2 rise" style="max-width:16ch">What is on the bench</h2>
    <p class="body rise d1" style="margin-top:1.5rem">Four products in active development. Each one started as a capability we could not stop thinking about.</p>
    <div class="cards">%(cards)s</div>
  </div>
</section>

<section class="closing section-b" data-ground="#100C0A">
  <div class="wrap">
    <h2 class="h2 rise">Building something where AI is the point?</h2>
    <p class="body rise d1">We take on a small number of partner builds each year, usually with operators who know a domain far better than we do.</p>
    <div class="rise d2">
      <a class="btn btn-primary btn-lg" href="mailto:hello@felixor.com?subject=Felixor">Start a conversation %(ar)s</a>
    </div>
  </div>
</section>
""" % dict(words=words, ar=AR, track=track, steps=steps_html, labs=labs_html,
           cards="".join(card(p) for p in PRODUCTS))

# ---------- portfolio ----------
portfolio = """
<section class="about-hero" data-ground="#0A0B0E">
  <div class="wrap">
    <h1 class="display rise in" style="max-width:14ch">Portfolio</h1>
    <p class="lead rise d1" style="margin-top:1.5rem; max-width:56ch">Four products in active development. Nothing here is generally available yet, so every link below is a placeholder until launch.</p>
    <div class="cards">%s</div>
  </div>
</section>
""" % "".join(card(p) for p in PRODUCTS)

# ---------- product pages ----------
def product_page(p):
    does = "".join('<li class="rise"><h4 class="h4">%s</h4><p>%s</p></li>' % (t,b) for t,b in p["does"])
    return """
<section class="phero" data-ground="#0A0B0E">
  <div class="wrap">
    <a class="back" href="#/portfolio">%(arr)s Portfolio</a>
    <div class="pmeta"><span class="chip">%(cat)s</span><span class="chip chip-dev">%(status)s</span></div>
    <h1 class="display rise in" style="max-width:12ch">%(name)s</h1>
    <p class="lead rise d1" style="margin-top:1.4rem">%(tag)s</p>
    <figure class="phero-art rise d2"><div class="art" style="--art:var(--art-%(artk)s)" role="img" aria-label="Generative artwork for %(name)s"></div></figure>
  </div>
</section>
<section class="section" data-ground="#0B0D12">
  <div class="wrap pgrid">
    <h2 class="h2 rise">The problem</h2>
    <div>
      <p class="body rise d1" style="font-size:1.15rem; color:var(--fg)">%(lede)s</p>
      <p class="body rise d2">%(problem)s</p>
    </div>
  </div>
</section>
<section class="section section-b" data-ground="#0C0A10">
  <div class="wrap pgrid">
    <h2 class="h2 rise">What it does</h2>
    <ul class="does">%(does)s</ul>
  </div>
</section>
<section class="section section-b" data-ground="#100C0A">
  <div class="wrap">
    <div class="cta-band rise">
      <div>
        <h3 class="h3">%(name)s is not public yet.</h3>
        <p class="small" style="margin-top:.5rem; max-width:46ch">This link goes live at launch. Until then, tell us what you would want it to do.</p>
      </div>
      <div style="display:flex; gap:.7rem; flex-wrap:wrap">
        <a class="btn btn-primary" href="#" aria-disabled="true" title="Placeholder link until launch">Visit %(name)s %(ar)s</a>
        <a class="btn btn-ghost" href="mailto:hello@felixor.com?subject=%(name)s">Get early access</a>
      </div>
    </div>
  </div>
</section>
""" % dict(arr=ARR, ar=AR, cat=p["cat"], status=p["status"], name=p["name"], tag=p["tag"],
           artk=p["art"], lede=p["lede"], problem=p["problem"], does=does)

# ---------- about ----------
timeline = "".join(
  '<li class="rise"><div class="org">%s</div><div><div class="role">%s</div>%s</div></li>'
  % (org, role, ('<div class="note">%s</div>' % note) if note else '')
  for org, role, note in CAREER)

about = """
<section class="about-hero" data-ground="#0A0B0E">
  <div class="wrap">
    <h1 class="display rise in" style="max-width:16ch">An AI product studio, run by people who have shipped at scale.</h1>
    <p class="lead rise d1" style="margin-top:1.6rem; max-width:56ch">Felixor exists because the interesting problem moved. It is no longer whether a model can do the thing. It is what to build now that it can.</p>
  </div>
</section>

<section class="section" data-ground="#0B0D12">
  <div class="wrap pgrid">
    <h2 class="h2 rise">The studio</h2>
    <div>
      <p class="body rise d1">We build products with AI at the core. Not products that added a chat panel, and not services that help someone else add one. Felixor conceives, designs, builds, and operates its own products, and takes a small number of partner builds each year with operators who bring a domain we could not learn fast enough on our own.</p>
      <p class="body rise d2">The studio model is a deliberate bet. AI products are unusually cheap to prototype and unusually expensive to get right, because the hard part arrives after the demo works: the evaluation, the failure modes, the trust, and the second session. A studio can carry a product through that stretch. A consultancy hands over a deck before it starts.</p>
      <p class="body rise d3">We stay small on purpose, we build in public where we can, and we would rather kill an idea in week three than defend it for a year.</p>
    </div>
  </div>
</section>

<section class="section section-b" data-ground="#0C0A10">
  <div class="wrap pgrid">
    <h2 class="h2 rise">The founder</h2>
    <div>
      <p class="body rise d1" style="font-size:1.15rem; color:var(--fg)">Felixor was founded by Curtis Lee, who has spent his career on the user-facing edge of large technical platforms and on the small teams trying to build the next one.</p>
      <p class="body rise d2">Most recently he was a Vice President at Microsoft, where he led Azure Experiences and Ecosystems: the product surface of Azure, including its AI surface areas. It is an unusual vantage point on this moment. Azure is where an enormous amount of the world's AI capability is actually provisioned, and the job was to decide what that capability should look like to the people using it. Before that he ran Global Payments at Microsoft.</p>
      <p class="body rise d3">He has been a founder twice. Luxe, an on-demand parking and valet service, was acquired by Volvo. Pinwheel is a leading fintech API for direct deposit and bill switching. Earlier he worked in Corporate Development at Stripe, ran consumer products as a Vice President at Groupon, and held product roles at Google, YouTube, and Zynga.</p>
      <p class="body rise d4">The through line is consumer-grade product instinct applied inside infrastructure companies, which is more or less the exact job an AI product studio has to do.</p>
      <div class="rise d4" style="margin-top:2rem">
        <a class="btn btn-ghost" href="https://www.linkedin.com/in/curtisylee/" target="_blank" rel="noopener">Curtis on LinkedIn %(ar)s</a>
      </div>
    </div>
  </div>
</section>

<section class="section section-b" data-ground="#0A0B0E">
  <div class="wrap pgrid">
    <h2 class="h2 rise">Before this</h2>
    <ul class="timeline">%(timeline)s</ul>
  </div>
</section>

<section class="closing section-b" data-ground="#100C0A">
  <div class="wrap">
    <h2 class="h2 rise">Work with the studio</h2>
    <p class="body rise d1">Partner builds, early access to what is on the bench, or a conversation about something you cannot stop thinking about.</p>
    <div class="rise d2"><a class="btn btn-primary btn-lg" href="mailto:hello@felixor.com?subject=Felixor">Start a conversation %(ar)s</a></div>
  </div>
</section>
""" % dict(ar=AR, timeline=timeline)

pages = ['<div class="page" id="page-home" data-title="Felixor">%s</div>' % home,
         '<div class="page" id="page-portfolio" data-title="Portfolio | Felixor">%s</div>' % portfolio,
         '<div class="page" id="page-about" data-title="About | Felixor">%s</div>' % about]
for p in PRODUCTS:
    pages.append('<div class="page" id="page-product-%s" data-title="%s | Felixor">%s</div>'
                 % (p["slug"], p["name"], product_page(p)))

FACE = "".join("@font-face{font-family:'%s';font-style:normal;font-weight:%s;font-display:swap;"
               "src:url(data:font/woff2;base64,%s) format('woff2');}" % (f["fam"], f["wght"], f["b64"])
               for f in fonts if f["fam"]=="Geist")

ARTVARS = ":root{" + "".join("--art-%s:url(%s);" % (k,v) for k,v in art.items()) + "}"

BODY = """<title>Felixor</title>
<style>%(face)s</style>
<style>%(artvars)s</style>
<style>%(css)s</style>
<noscript><style>
  .page{display:none !important} #page-home{display:block !important}
  .rise,.pop,.hero-lag{opacity:1 !important; transform:none !important}
  .w > span{transform:none !important}
  .rule{width:110px !important}
  .step-n{opacity:1} .step h3{color:var(--fg)} .step p{opacity:1; color:var(--fg-2)}
  #mesh,#story-canvas{display:none}
  .vis-frame{background:linear-gradient(150deg,#15171E,#0A0B0E)}
</style></noscript>
<a class="skip" href="#main">Skip to content</a>
<div class="ground" aria-hidden="true"></div>
<header class="nav" id="nav">
  <div class="wrap">
    <a href="#/" class="mark" aria-label="Felixor, home">Felixor<i>.</i></a>
    <nav class="navlinks" aria-label="Primary">
      <span class="navpill" aria-hidden="true"></span>
      <a href="#/">Studio</a>
      <a href="#/portfolio">Portfolio</a>
      <a href="#/about">About</a>
    </nav>
    <a href="mailto:hello@felixor.com?subject=Felixor" class="btn btn-primary navcta" style="padding:.58rem .95rem;font-size:.875rem">Get in touch</a>
  </div>
</header>
<main id="main">%(pages)s</main>
<footer class="footer">
  <div class="wrap">
    <div>
      <a href="#/" class="mark">Felixor<i>.</i></a>
      <p class="legal" style="margin-top:.6rem; max-width:24ch">An AI product studio.</p>
    </div>
    <div class="cols">
      <div><h4>Studio</h4><ul>
        <li><a href="#/portfolio">Portfolio</a></li>
        <li><a href="#/about">About</a></li>
      </ul></div>
      <div><h4>Products</h4><ul>%(plinks)s</ul></div>
      <div><h4>Contact</h4><ul>
        <li><a href="mailto:hello@felixor.com">hello@felixor.com</a></li>
        <li><a href="https://www.linkedin.com/in/curtisylee/" target="_blank" rel="noopener">LinkedIn</a></li>
      </ul></div>
    </div>
    <p class="legal">&copy; 2026 Felixor</p>
  </div>
</footer>
<script>%(js)s</script>
""" % dict(face=FACE, css=css, pages="".join(pages), js=js,
           artvars=ARTVARS,
           plinks="".join('<li><a href="#/product/%s">%s</a></li>' % (p["slug"], p["name"]) for p in PRODUCTS))

open(_r("artifact.html"),"w").write(BODY)

DESC = "Felixor is an AI product studio. We design, build, and ship products where the intelligence is the foundation, not a feature."
head = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="%(d)s">
<meta name="theme-color" content="#0A0B0E">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="canonical" href="https://www.felixor.com/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Felixor">
<meta property="og:title" content="Felixor">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://www.felixor.com/">
<meta name="twitter:card" content="summary_large_image">
""" % dict(d=DESC)
open(_r("index.html"),"w").write(head + BODY.replace("<title>Felixor</title>","<title>Felixor</title>\n</head>\n<body>",1) + "\n</body>\n</html>\n")
print(PAL_NAME, "artifact.html", round(len(open(_r('artifact.html')).read())/1024), "KB")
print("index.html   ", round(len(open(_r('index.html')).read())/1024), "KB")
