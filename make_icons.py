"""App icon in every size, the maskable version and the favicon, from one drawing.

    python3 make_icons.py docs

bible-study only. New River keeps its own dove icons (see WORKFLOW.md)."""
import sys, io
from playwright.sync_api import sync_playwright
from PIL import Image

out = sys.argv[1]  # bible-study docs dir
G, BG = "#e9c46f", "#33241a"
ART = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="{{s}}" height="{{s}}"><rect width="512" height="512" fill="{BG}"/>
<rect x="238" y="104" width="36" height="262" rx="5" fill="{G}"/><rect x="170" y="176" width="172" height="36" rx="5" fill="{G}"/>
<path d="M108 352C156 330 216 334 256 366C296 334 356 330 404 352" fill="none" stroke="{G}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M108 392C156 370 216 374 256 406C296 374 356 370 404 392" fill="none" stroke="{G}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
# favicon: just the cross, heavier, so it survives at 16px
FAV = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="{{s}}" height="{{s}}"><rect width="64" height="64" rx="12" fill="{BG}"/>
<rect x="27" y="10" width="10" height="44" rx="2" fill="{G}"/><rect x="17" y="21" width="30" height="10" rx="2" fill="{G}"/></svg>'''

def render(pw_page, svg, size):
    pw_page.set_content(f'<body style="margin:0;background:transparent">{svg.format(s=size)}</body>')
    return Image.open(io.BytesIO(pw_page.screenshot(clip={"x": 0, "y": 0, "width": size, "height": size}, omit_background=True))).convert("RGBA")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 600, "height": 600})
    for name, size in (("icon-512.png", 512), ("icon-192.png", 192), ("icon-maskable-512.png", 512), ("apple-touch-icon.png", 180)):
        im = render(pg, ART, size).convert("RGB")
        im.save(f"{out}/site/{name}", optimize=True)
    fav = {s: render(pg, FAV, s) for s in (16, 32, 48)}
    fav[48].save(f"{out}/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)], append_images=[fav[32], fav[16]])
    fav[32].save(f"{out}/site/favicon-32.png", optimize=True)
    b.close()
print("icons written")
