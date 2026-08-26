import re, base64, os, json, shutil
html = open("index.html").read()
os.path.exists("dist") and shutil.rmtree("dist")
os.makedirs("dist/assets", exist_ok=True)
manifest = {}

# fonts: two @font-face data URIs, in declaration order
fonts = re.findall(r"@font-face\{font-family:'([^']+)';[^}]*?url\(data:font/woff2;base64,([A-Za-z0-9+/=]+)\)", html)
for fam, b64 in fonts:
    name = fam.lower().replace(" ", "-") + ".woff2"
    open("dist/assets/"+name, "wb").write(base64.b64decode(b64))
    html = html.replace("data:font/woff2;base64," + b64, "/assets/" + name)
    manifest[name] = len(base64.b64decode(b64))

# artwork: --art-<key>:url(data:image/webp;base64,...)
for key, b64 in re.findall(r"--art-([a-z]+):url\(data:image/webp;base64,([A-Za-z0-9+/=]+)\)", html):
    name = key + ".webp"
    open("dist/assets/"+name, "wb").write(base64.b64decode(b64))
    html = html.replace("data:image/webp;base64," + b64, "/assets/" + name)
    manifest[name] = len(base64.b64decode(b64))

open("dist/index.html","w").write(html)
open("dist/vercel.json","w").write(json.dumps({
  "cleanUrls": True,
  "headers": [
    {"source": "/assets/(.*)",
     "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
    {"source": "/(.*)",
     "headers": [
       {"key": "X-Content-Type-Options", "value": "nosniff"},
       {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"}]}
  ]
}, indent=2))
open("dist/robots.txt","w").write("User-agent: *\nAllow: /\nSitemap: https://www.felixor.com/sitemap.xml\n")
open("dist/sitemap.xml","w").write(
 '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
 + '  <url><loc>https://www.felixor.com/</loc><priority>1.0</priority></url>\n</urlset>\n')
print("index.html", len(html)//1024, "KB")
for k,v in manifest.items(): print("  assets/"+k, v//1024, "KB")
print("remaining data URIs:", len(re.findall(r"data:(?:font|image)", html)))
