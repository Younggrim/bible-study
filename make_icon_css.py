"""Self-hosted replacement for Font Awesome: ~35 icons drawn here, written into
site/style.css as CSS masks, so the pages keep their <i class="fas fa-..."> markup
and nothing is fetched from a CDN.

    python3 make_icon_css.py docs/site/style.css [more style.css ...]

Idempotent: rewrites the block between the two marker comments. To add an icon,
add it to ICONS (24x24 grid; stroke icons use S, solid ones use F) and rerun on
both sites' style.css. Everything is drawn in black; the colour comes from the
element's own text colour."""
import re, sys, urllib.parse

S = lambda d: f'<g fill="none" stroke="#000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{d}</g>'
F = lambda d: f'<g fill="#000">{d}</g>'
P = lambda d: f'<path d="{d}"/>'

ICONS = {
    "book": S(P("M5 5A2 2 0 0 1 7 3H19V18H7A2 2 0 0 0 5 20Z") + P("M5 20A2 2 0 0 0 7 21H19V18")),
    "book-open": S(P("M2 5c3-1 7-1 10 1 3-2 7-2 10-1v14c-3-1-7-1-10 1-3-2-7-2-10-1Z") + P("M12 6v14")),
    "book-bible": S(P("M5 5A2 2 0 0 1 7 3H19V21H7A2 2 0 0 1 5 19Z") + P("M12 7V14.5") + P("M9.2 9.7H14.8")),
    "home": S(P("M3 11.5 12 3.5l9 8") + P("M5.5 10v10.5h4.5V15h4v5.5h4.5V10")),
    "bars": S(P("M4 6H20") + P("M4 12H20") + P("M4 18H20")),
    "arrow-left": S(P("M20 12H4") + P("M10 6l-6 6 6 6")),
    "arrow-right": S(P("M4 12H20") + P("M14 6l6 6-6 6")),
    "chevron-left": S(P("M15 5l-7 7 7 7")),
    "chevron-right": S(P("M9 5l7 7-7 7")),
    "youtube": S('<rect x="2" y="5" width="20" height="14" rx="4"/>') + F(P("M10 9l5 3-5 3Z")),
    "bookmark": F(P("M6 3H18V21L12 16.5 6 21Z")),
    "far-bookmark": S(P("M6.5 3.5H17.5V19.5L12 15.5 6.5 19.5Z")),
    "user": F('<circle cx="12" cy="7.5" r="4.5"/>' + P("M3.5 21c0-4.6 3.8-7.5 8.5-7.5s8.5 2.9 8.5 7.5Z")),
    "far-user": S('<circle cx="12" cy="8" r="4"/>' + P("M4.5 20.5c0-4 3.4-6.5 7.5-6.5s7.5 2.5 7.5 6.5Z")),
    "user-check": S('<circle cx="9" cy="8" r="4"/>' + P("M2.5 20.5c0-4 3-6.5 6.5-6.5") + P("M14.5 17l2.5 2.5 4.5-5")),
    "share-nodes": S('<circle cx="18" cy="5.5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="18.5" r="2.5"/>' + P("M8.2 10.8l7.6-4.1") + P("M8.2 13.2l7.6 4.1")),
    "play": F(P("M7 4l13 8-13 8Z")),
    "pause": F('<rect x="6" y="4" width="4.5" height="16" rx="1"/><rect x="13.5" y="4" width="4.5" height="16" rx="1"/>'),
    "fire": F(P("M12.5 2C13.5 6 17.5 8 17.5 13A5.5 5.5 0 0 1 6.5 13C6.5 10.8 7.5 9.5 8.8 8.4 8.8 10.2 9.6 11.2 10.8 11.4 10 7.5 10.8 4.8 12.5 2Z")),
    "hands-praying": S(P("M3 18H21") + P("M7 18A5 5 0 0 1 17 18") + P("M12 6V9") + P("M5 10.5L7 12.5") + P("M19 10.5L17 12.5") + P("M8 21.5H16")),
    "comments": S(P("M3 5H16V14H8.5L5 17V14H3Z") + P("M19 9H21V18H20V21L17 18H11V16")),
    "check": S(P("M4 12.5l5 5L20 6.5")),
    "bell": S(P("M6 17V11a6 6 0 0 1 12 0v6l2 2H4Z") + P("M10 21.5h4")),
    "trash": S(P("M4 7H20") + P("M9 7V4H15V7") + P("M6 7l1 14H17L18 7") + P("M10 11v6") + P("M14 11v6")),
    "spinner": S(P("M12 3a9 9 0 1 0 9 9")),
    "plus": S(P("M12 5v14") + P("M5 12H19")),
    "pen-to-square": S(P("M11 4H5A1 1 0 0 0 4 5V19A1 1 0 0 0 5 20H19A1 1 0 0 0 20 19V13") + P("M18 3l3 3-9 9-4 1 1-4Z")),
    "list-ul": S(P("M9 6H21") + P("M9 12H21") + P("M9 18H21")) + F('<circle cx="4.5" cy="6" r="1.5"/><circle cx="4.5" cy="12" r="1.5"/><circle cx="4.5" cy="18" r="1.5"/>'),
    "list-ol": S(P("M10 6H21") + P("M10 12H21") + P("M10 18H21") + P("M3.5 4.5L5 4V8") + P("M3.5 11h2.5L3.5 14H6") + P("M3.5 17h2.5v1.5H4.5 6V20H3.500")),
    "lightbulb": S(P("M12 3A6 6 0 0 0 8.400 13.800C9.100 14.400 9.500 15.200 9.500 16H14.500C14.500 15.200 14.900 14.400 15.600 13.800A6 6 0 0 0 12 3Z") + P("M9.500 18.500H14.500") + P("M10.500 21H13.500")),
    "language": S(P("M4 5h9") + P("M8.500 3v2") + P("M6 5c1 4 3.500 7 6.500 9") + P("M11.500 5c-1 4-4 7-7.500 9") + P("M13 21l4.500-11L22 21") + P("M14.500 17.500h6")),
    "heart": F(P("M12 20.500C5.500 15.900 3 12.500 3 9.100A4.600 4.600 0 0 1 12 7.100A4.600 4.600 0 0 1 21 9.100C21 12.500 18.500 15.900 12 20.500Z")),
    "eraser": S(P("M20 20H9L4 15 15 4l6 6-8 8") + P("M8 11l6 6")),
    "bullseye": S('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.500"/>') + F('<circle cx="12" cy="12" r="1.200"/>'),
    "cross": S(P("M12 3V21") + P("M6 9H18")),
    "circle-info": S('<circle cx="12" cy="12" r="9"/>' + P("M12 11v6")) + F('<circle cx="12" cy="7.500" r="1.300"/>'),
}
ICONS["list-ol"] = S(P("M10 6H21") + P("M10 12H21") + P("M10 18H21") + P("M3.5 4.5L5 4V8") + P("M3.5 11.5h2.500L3.500 14.500H6") + P("M3.500 17h2.500v1.500H4.500 6V20H3.500"))
ICONS["list-ol"] = S(P("M10 6H21") + P("M10 12H21") + P("M10 18H21") + P("M3.5 4.5L5 4V8") + P("M3.5 11.5h2.5l-2.5 3H6") + P("M3.5 17h2.5v1.5H4.5h1.5V20H3.5"))

BEGIN = "/* ===== Icons (self-hosted; replaces Font Awesome) ====="
END = "/* ===== end icons ===== */"


def uri(inner):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">{inner}</svg>'
    return "url(\"data:image/svg+xml," + urllib.parse.quote(svg, safe="/:=,() ").replace(" ", "%20").replace('"', "'") + "\")"


def block():
    out = [BEGIN, "   Same class names as before, so no page or script had to change. Each icon is a",
           "   mask filled with the element's text colour. Regenerate: python3 make_icon_css.py */",
           ".fas, .far, .fab { display: inline-block; width: 1em; height: 1em; flex: none; vertical-align: -0.125em; font-style: normal; line-height: 1; background-color: currentColor; -webkit-mask: var(--ico) center / contain no-repeat; mask: var(--ico) center / contain no-repeat; }"]
    for name, inner in ICONS.items():
        sel = f".far.fa-{name[4:]}" if name.startswith("far-") else f".fa-{name}"
        out.append(f"{sel} {{ --ico: {uri(inner)}; }}")
    out.append(".fa-spin { animation: fa-spin 1s linear infinite; }")
    out.append("@keyframes fa-spin { to { transform: rotate(360deg); } }")
    out.append("@media (prefers-reduced-motion: reduce) { .fa-spin { animation-duration: 3s; } }")
    out.append(END)
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    for path in sys.argv[1:]:
        s = open(path, encoding="utf-8").read()
        s = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", "", s, flags=re.S).rstrip("\n") + "\n\n" + block()
        open(path, "w", encoding="utf-8").write(s)
        print("icons written to", path)
