# name: (accent, accent-2 hover, secondary for art/mesh, deep tone, btn text)
PALETTES = {
 "iris":     dict(accent="#6C6CF0", a2="#8A8AFB", sec="#3FA9C9", deep="#3A2E8C", btn="#FFFFFF", btn_bg="#5B5AE8", label="Iris"),
 "glacier":  dict(accent="#4FB3E8", a2="#7ACBF2", sec="#6C6CF0", deep="#1E5A85", btn="#04141C", btn_bg="#4FB3E8", label="Glacier"),
 "amethyst": dict(accent="#9B72E0", a2="#B492EE", sec="#4F8FD6", deep="#4A2C7A", btn="#FFFFFF", btn_bg="#7E52CC", label="Amethyst"),
}
def rgb(h): h=h.lstrip("#"); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def lum(h):
    def f(c):
        c/=255; return c/12.92 if c<=.03928 else ((c+.055)/1.055)**2.4
    r,g,b=rgb(h); return .2126*f(r)+.7152*f(g)+.0722*f(b)
def contrast(a,b):
    la,lb=lum(a),lum(b); hi,lo=max(la,lb),min(la,lb); return (hi+.05)/(lo+.05)
if __name__=="__main__":
    for k,p in PALETTES.items():
        print(k.ljust(9), "btn text on accent:", round(contrast(p["accent"],p["btn"]),2),
              "| accent on bg:", round(contrast(p["accent"],"#0A0B0E"),2))
