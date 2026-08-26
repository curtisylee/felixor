import math, random, io, base64, json
from PIL import Image, ImageDraw, ImageFilter, ImageChops
W,H=1200,800
import sys
from palettes import PALETTES, rgb
PAL = PALETTES[sys.argv[1] if len(sys.argv)>1 else "iris"]
BG=(10,11,14); EMBER=rgb(PAL["accent"]); RUST=rgb(PAL["deep"]); SLATE=rgb(PAL["sec"]); BONE=(226,224,220)

def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
def canvas(): return Image.new("RGB",(W,H),BG)

def glow(img, r=26, amt=.75):
    return ImageChops.screen(img, img.filter(ImageFilter.GaussianBlur(r)).point(lambda v:int(v*amt)))

# 1. Quorum: interference rings converging on agreement
def quorum(seed=3):
    random.seed(seed); im=canvas(); d=ImageDraw.Draw(im,"RGBA")
    centers=[(W*.32,H*.44),(W*.62,H*.38),(W*.5,H*.72)]
    for ci,(cx,cy) in enumerate(centers):
        col = [EMBER,SLATE,RUST][ci]
        for i in range(26):
            r=26+i*29
            a=int(210*(1-i/26)**1.2)+14
            d.ellipse([cx-r,cy-r,cx+r,cy+r], outline=col+(a,), width=2 if i<8 else 1)
    return glow(im,22,.8)

# 2. Camber: a flow field, motion finding its line
def camber(seed=11):
    random.seed(seed); im=canvas(); d=ImageDraw.Draw(im,"RGBA")
    def field(x,y):
        return (math.sin(x*.0042)+math.cos(y*.0051)*1.3+math.sin((x+y)*.0022))*1.5
    for n in range(1500):
        x=random.uniform(-100,W+100); y=random.uniform(-60,H+60)
        t=random.random(); col=lerp(SLATE,EMBER,t**1.6); a=int(26+90*t**2)
        pts=[]
        for s in range(56):
            pts.append((x,y)); ang=field(x,y); x+=math.cos(ang)*7; y+=math.sin(ang)*7
            if not(-140<x<W+140 and -100<y<H+100): break
        if len(pts)>3: d.line(pts, fill=col+(a,), width=1)
    return glow(im,20,.55)

# 3. Understory: strata, knowledge in layers
def understory(seed=7):
    random.seed(seed); im=canvas(); d=ImageDraw.Draw(im,"RGBA")
    for L in range(30):
        t=L/29; base=H*.16+t*H*.78
        col=lerp(SLATE,EMBER,t**1.5); a=int(70+150*t**1.1)
        pts=[]
        ph=random.uniform(0,9); amp=16+58*(1-t)
        for x in range(-20,W+20,5):
            y=base+math.sin(x*.0037+ph)*amp+math.sin(x*.0091+ph*2)*amp*.38
            pts.append((x,y))
        d.line(pts, fill=col+(a,), width=1 if t<.7 else 2)
    return glow(im,22,.6)

# 4. Tidemark: standing waves, signal against noise
def tidemark(seed=19):
    random.seed(seed); im=canvas(); d=ImageDraw.Draw(im,"RGBA")
    cx,cy=W*.5,H*.5
    for i in range(150):
        t=i/149
        col=lerp(RUST,EMBER,t) if i%3 else lerp(SLATE,BONE,t*.5)
        a=int(16+108*(1-abs(t-.5)*1.7))
        pts=[]
        for x in range(-10,W+10,4):
            u=(x-cx)/W
            y=cy+math.sin(u*13+t*7)*(H*.30)*math.exp(-abs(u)*1.5)+ (t-.5)*H*.92
            pts.append((x,y))
        d.line(pts, fill=col+(max(a,0),), width=1)
    return glow(im,24,.62)

MAKE={"quorum":quorum,"camber":camber,"understory":understory,"tidemark":tidemark}
out={}
for k,f in MAKE.items():
    im=f()
    # vignette so each sits into the page ground
    m=Image.new("L",(W,H),0); ImageDraw.Draw(m).ellipse([-W*.3,-H*.3,W*1.3,H*1.3],fill=255)
    m=m.filter(ImageFilter.GaussianBlur(190))
    im=Image.composite(im, Image.blend(im,Image.new("RGB",(W,H),BG),.72), m)
    buf=io.BytesIO(); im.save(buf,"WEBP",quality=80,method=6)
    out[k]="data:image/webp;base64,"+base64.b64encode(buf.getvalue()).decode()
    im.resize((300,200)).save(f"/tmp/art_{k}.png")
    print(k, len(buf.getvalue())//1024, "KB")
json.dump(out,open("art.json","w"))
sheet=Image.new("RGB",(604,404),(16,16,18))
for i,k in enumerate(MAKE):
    sheet.paste(Image.open(f"/tmp/art_{k}.png"),((i%2)*302,(i//2)*202))
sheet.save("/tmp/artsheet.png")
