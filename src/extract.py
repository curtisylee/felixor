"""Split the self-contained index.html into index.html + assets/.

build.py inlines every font and image as a data URI. That is convenient for a
single-file preview but wasteful to serve, so this pulls them back out into
cacheable files and rewrites the references. Also subsets the font down to the
characters the site actually uses.

Run after build.py. Writes in place at the repo root.
"""
import base64
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
INDEX = os.path.join(ROOT, "index.html")

# Latin-1 plus smart quotes and dashes. Widen this if copy ever needs more.
SUBSET_RANGE = "U+0020-007E,U+00A0-00FF,U+2018-201D,U+2013,U+2014,U+2026,U+00D7"


def main():
    html = open(INDEX, encoding="utf-8").read()
    if os.path.isdir(ASSETS):
        shutil.rmtree(ASSETS)
    os.makedirs(ASSETS)
    written = []

    for family, b64 in re.findall(
        r"@font-face\{font-family:'([^']+)';[^}]*?url\(data:font/woff2;base64,([A-Za-z0-9+/=]+)\)",
        html,
    ):
        name = family.lower().replace(" ", "-") + ".woff2"
        path = os.path.join(ASSETS, name)
        open(path, "wb").write(base64.b64decode(b64))
        html = html.replace("data:font/woff2;base64," + b64, "/assets/" + name)
        subset(path)
        written.append(name)

    for key, b64 in re.findall(
        r"--art-([a-z]+):url\(data:image/webp;base64,([A-Za-z0-9+/=]+)\)", html
    ):
        name = key + ".webp"
        open(os.path.join(ASSETS, name), "wb").write(base64.b64decode(b64))
        html = html.replace("data:image/webp;base64," + b64, "/assets/" + name)
        written.append(name)

    leftover = len(re.findall(r"data:(?:font|image)/", html))
    if leftover:
        sys.exit("ERROR: %d data URIs left in index.html" % leftover)

    open(INDEX, "w", encoding="utf-8").write(html)

    print("index.html %d KB" % (len(html.encode()) // 1024))
    for name in written:
        print("  assets/%s %d KB" % (name, os.path.getsize(os.path.join(ASSETS, name)) // 1024))

    missing = [
        ref for ref in sorted(set(re.findall(r"/assets/[\w.-]+", html)))
        if not os.path.isfile(os.path.join(ROOT, ref.lstrip("/")))
    ]
    if missing:
        sys.exit("ERROR: unresolved asset references: %s" % missing)
    print("all asset references resolve")


def subset(path):
    """Shrink the font to the characters in use. Skipped if fonttools is absent."""
    tmp = path + ".full"
    os.rename(path, tmp)
    try:
        subprocess.run(
            ["pyftsubset", tmp, "--output-file=" + path, "--flavor=woff2",
             "--unicodes=" + SUBSET_RANGE,
             "--layout-features=kern,liga,calt,tnum,onum,ss01", "--no-hinting"],
            check=True, capture_output=True,
        )
        os.remove(tmp)
    except (FileNotFoundError, subprocess.CalledProcessError):
        os.rename(tmp, path)
        print("  (pyftsubset unavailable, shipping the full font)")


if __name__ == "__main__":
    main()
