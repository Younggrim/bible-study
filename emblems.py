"""Line emblems for the study banners. 64x64 viewBox, drawn with stroke only.
Stroke width, colour and caps come from CSS (.hero-emblem svg), so these hold
paths and nothing else. Keys are page filenames without .html."""
import math


def _ring(n, cx, cy, r, dot):
    out = []
    for i in range(n):
        a = -math.pi / 2 + i * 2 * math.pi / n
        out.append(f'<circle cx="{cx + r * math.cos(a):.1f}" cy="{cy + r * math.sin(a):.1f}" r="{dot}"/>')
    return "".join(out)


def _wheat():
    parts = ['<path d="M32 58V10"/>', '<path d="M32 10C29 14 29 18 32 22C35 18 35 14 32 10Z"/>']
    for y in (26, 38, 50):
        parts.append(f'<path d="M32 {y}C25 {y} 20 {y-5} 20 {y-12}C27 {y-12} 32 {y-7} 32 {y}Z"/>')
        parts.append(f'<path d="M32 {y}C39 {y} 44 {y-5} 44 {y-12}C37 {y-12} 32 {y-7} 32 {y}Z"/>')
    return "".join(parts)


E = {
    # ---- life studies -------------------------------------------------------
    "addiction": '<rect x="6" y="34" width="26" height="14" rx="7" transform="rotate(-38 19 41)"/><rect x="32" y="16" width="26" height="14" rx="7" transform="rotate(-38 45 23)"/><path d="M27 21L23 16"/><path d="M33 26L33 20"/><path d="M38 32L44 33"/>',
    "anger": '<path d="M6 42H58"/><path d="M20 42A12 12 0 0 1 44 42"/><path d="M32 17V23"/><path d="M14.5 24.5L19 29"/><path d="M49.5 24.5L45 29"/><path d="M8 34H13"/><path d="M51 34H56"/><path d="M16 50H48"/><path d="M25 57H39"/>',
    "anxiety-and-fear": '<path d="M17 38A9 9 0 0 1 19 21A12 12 0 0 1 42 19A10 10 0 0 1 47 38Z"/><path d="M34 38L27 48H35L29 58"/>',
    "depression-and-hopelessness": '<path d="M32 7C38 14 39 20 32 27C25 20 26 14 32 7Z"/><path d="M32 27V32"/><path d="M26 32H38V54H26Z"/><path d="M20 54H44"/>',
    "doubt-and-unbelief": '<path d="M22 24C22 16 27 11 33 11C40 11 44 16 44 21C44 28 36 29 33 35V38"/><circle cx="33" cy="50" r="2.2" fill="currentColor" stroke="none"/>',
    "greed-and-materialism": '<ellipse cx="32" cy="19" rx="16" ry="6"/><path d="M16 19V28C16 31.3 23 34 32 34C41 34 48 31.3 48 28V19"/><path d="M16 28V37C16 40.3 23 43 32 43C41 43 48 40.3 48 37V28"/><path d="M16 37V46C16 49.3 23 52 32 52C41 52 48 49.3 48 46V37"/>',
    "grief-and-loss": '<path d="M32 7C32 7 16 24 16 37A16 16 0 0 0 48 37C48 24 32 7 32 7Z"/><path d="M24 39A8 8 0 0 0 31 47"/>',
    "identity-and-self-worth": '<path d="M19 11H45L57 26L32 55L7 26Z"/><path d="M7 26H57"/><path d="M25 11L20 26L32 55L44 26L39 11"/>',
    "loneliness": '<path d="M40 9A23 23 0 1 0 55 41A19 19 0 0 1 40 9Z"/><path d="M46 12V20"/><path d="M42 16H50"/><path d="M54 26V32"/><path d="M51 29H57"/>',
    "lust-and-sexual-sin": '<path d="M32 8C39 16 39 28 32 38C25 28 25 16 32 8Z"/><path d="M32 38C23 36 15 29 13 19C23 19 30 26 32 38Z"/><path d="M32 38C41 36 49 29 51 19C41 19 34 26 32 38Z"/><path d="M32 38V57"/><path d="M32 52C26 52 22 49 20 44"/>',
    "pride": '<circle cx="32" cy="23" r="17"/><circle cx="32" cy="23" r="12.5"/><path d="M32 40V50"/><path d="M26 50H38V57H26Z"/><path d="M24 19A9 9 0 0 1 30 14"/>',
    "suffering": '<path d="M32 6C34 17 47 22 47 37C47 47 40 56 32 56C24 56 17 47 17 37C17 29 23 25 25 17C28 21 30 20 32 6Z"/><path d="M32 56C26 56 24 50 27 45C29 42 32 39 32 36C34 40 39 42 39 48C39 52 36 56 32 56Z"/>',
    "temptation": '<path d="M32 22C26 16 14 20 14 34C14 46 22 56 28 56C30 56 31 55 32 55C33 55 34 56 36 56C42 56 50 46 50 34C50 20 38 16 32 22Z"/><path d="M32 22C32 16 34 12 38 9"/><path d="M38 9C42 7 47 9 48 14C43 16 40 14 38 9Z"/>',
    "unforgiveness-and-bitterness": '<circle cx="21" cy="21" r="10"/><circle cx="21" cy="21" r="3"/><path d="M28 28L54 54"/><path d="M43 43L49 37"/><path d="M49 49L54 44"/>',
    # ---- topical studies ----------------------------------------------------
    "armor-of-god": '<path d="M32 7L52 14V30C52 43 43.5 52 32 57C20.5 52 12 43 12 30V14Z"/><path d="M32 19V45"/><path d="M22.5 28.5H41.5"/>',
    "attributes-of-god": '<circle cx="32" cy="32" r="10"/><path d="M32 6V14"/><path d="M32 50V58"/><path d="M6 32H14"/><path d="M50 32H58"/><path d="M13.6 13.6L19.3 19.3"/><path d="M44.7 44.7L50.4 50.4"/><path d="M13.6 50.4L19.3 44.7"/><path d="M44.7 19.3L50.4 13.6"/>',
    "beatitudes": '<path d="M5 52L24 22L34 37L42 26L59 52Z"/><circle cx="48" cy="13" r="5"/><path d="M24 22L28 28L21 29"/>',
    "covenants": '<path d="M6 48A26 26 0 0 1 58 48"/><path d="M14 48A18 18 0 0 1 50 48"/><path d="M22 48A10 10 0 0 1 42 48"/><path d="M4 56H60"/>',
    "fruits-of-the-spirit": '<path d="M32 24V10"/><path d="M32 14C37 7 46 6 52 10C48 17 39 19 32 14Z"/><circle cx="22.5" cy="31" r="5"/><circle cx="32" cy="31" r="5"/><circle cx="41.5" cy="31" r="5"/><circle cx="27.25" cy="40" r="5"/><circle cx="36.75" cy="40" r="5"/><circle cx="32" cy="49" r="5"/>',
    "gifts-of-the-holy-spirit": '<path d="M10 26H54V35H10Z"/><path d="M14 35V56H50V35"/><path d="M32 26V56"/><path d="M32 26C26 14 15 18 21 26"/><path d="M32 26C38 14 49 18 43 26"/>',
    "i-am-statements": '<path d="M38 58V24C38 15 32 9 24 9C16 9 11 15 11 21"/><path d="M30 58H46"/><path d="M11 21L16 25"/>',
    "judges-of-israel": '<path d="M32 8V54"/><path d="M20 54H44"/><path d="M12 18H52"/><path d="M12 18L5 36H19Z"/><path d="M52 18L45 36H59Z"/><path d="M5 36A7 5 0 0 0 19 36"/><path d="M45 36A7 5 0 0 0 59 36"/><circle cx="32" cy="12" r="3"/>',
    "kings-of-israel": '<path d="M10 44L6 21L21 31L32 12L43 31L58 21L54 44Z"/><path d="M10 52H54"/>',
    "men-of-the-bible": '<circle cx="32" cy="20" r="10"/><path d="M12 56C12 43 20 36 32 36C44 36 52 43 52 56"/><path d="M26 25C28 29 36 29 38 25"/>',
    "miracles-of-jesus": '<path d="M7 32C16 18 34 17 44 27L58 18V46L44 37C34 47 16 46 7 32Z"/><circle cx="20" cy="30" r="2" fill="currentColor" stroke="none"/><path d="M30 25C32 30 32 34 30 39"/>',
    "names-of-god": '<path d="M20 12H48V45A9 9 0 0 1 39 54H15A9 9 0 0 0 20 45Z"/><path d="M15 54A9 9 0 0 1 6 45V41H20"/><path d="M27 22H41"/><path d="M27 30H41"/><path d="M27 38H35"/>',
    "parables-of-jesus": _wheat(),
    "prayers-in-the-bible": '<path d="M12 36H52C52 47 43 54 32 54C21 54 12 47 12 36Z"/><path d="M24 56H40"/><path d="M24 29C20 25 28 21 24 15"/><path d="M32 29C28 25 36 21 32 12"/><path d="M40 29C36 25 44 21 40 15"/>',
    "promises-of-god": '<path d="M32 7L38.5 23.5L56 25L42.5 36.5L46.5 54L32 44.5L17.5 54L21.5 36.5L8 25L25.5 23.5Z"/>',
    "prophecy-and-fulfillment": '<circle cx="28" cy="36" r="22"/><circle cx="28" cy="36" r="14"/><circle cx="28" cy="36" r="6"/><path d="M28 36L55 9"/><path d="M55 9H46"/><path d="M55 9V18"/>',
    "spiritual-disciplines": '<path d="M32 56V32"/><path d="M32 38C23 38 17 32 17 24C26 24 32 29 32 38Z"/><path d="M32 30C41 30 47 24 47 16C38 16 32 21 32 30Z"/><path d="M14 56H50"/>',
    "ten-commandments": '<path d="M8 56V22A11 11 0 0 1 30 22V56Z"/><path d="M34 56V22A11 11 0 0 1 56 22V56Z"/><path d="M14 28H24"/><path d="M14 36H24"/><path d="M14 44H24"/><path d="M40 28H50"/><path d="M40 36H50"/><path d="M40 44H50"/>',
    "the-12-apostles": _ring(12, 32, 32, 22, 3.6) + '<path d="M32 21V43"/><path d="M24 28H40"/>',
    "the-gospel": '<path d="M32 8V56"/><path d="M19 22H45"/><path d="M22 12L17 7"/><path d="M42 12L47 7"/><path d="M12 30L6 28"/><path d="M52 30L58 28"/>',
    "the-trinity": '<circle cx="32" cy="24" r="13"/><circle cx="22.5" cy="40" r="13"/><circle cx="41.5" cy="40" r="13"/>',
    "types-of-christ": '<path d="M20 57V16"/><path d="M44 57V16"/><path d="M13 16H51"/><path d="M13 57H51"/><circle cx="26" cy="16" r="2.2" fill="currentColor" stroke="none"/><circle cx="32" cy="16" r="2.2" fill="currentColor" stroke="none"/><circle cx="38" cy="16" r="2.2" fill="currentColor" stroke="none"/><circle cx="20" cy="30" r="2.2" fill="currentColor" stroke="none"/><circle cx="20" cy="42" r="2.2" fill="currentColor" stroke="none"/><circle cx="44" cy="30" r="2.2" fill="currentColor" stroke="none"/><circle cx="44" cy="42" r="2.2" fill="currentColor" stroke="none"/>',
    "women-of-the-bible": '<circle cx="32" cy="15" r="8"/><path d="M24 17C21 24 21 31 25 35"/><path d="M40 17C43 24 43 31 39 35"/><path d="M32 25L22 35L10 57H54L42 35Z"/>',
}

# Banner emblems for the home page and its three section heroes (same marks
# as the app's tab bar, so the sections read the same everywhere).
SECTION = {
    "home": '<path d="M32 27C26 22 16 22 9 25V50C16 47 26 47 32 52C38 47 48 47 55 50V25C48 22 38 22 32 27Z"/><path d="M32 27V52"/><path d="M32 8V17"/><path d="M19 11L23 18"/><path d="M45 11L41 18"/>',
    "bible": '<path d="M13 13A5 5 0 0 1 18 8H51V56H18A5 5 0 0 1 13 51Z"/><path d="M32 17V36"/><path d="M24 25H40"/><path d="M13 51A5 5 0 0 1 18 46H51"/>',
    "topical": '<path d="M32 8A15 15 0 0 0 23 35C25 37 26 39 26 42H38C38 39 39 37 41 35A15 15 0 0 0 32 8Z"/><path d="M26 47H38"/><path d="M28 53H36"/>',
    "life": '<path d="M32 54C14 42 8 33 8 24A12 12 0 0 1 32 18A12 12 0 0 1 56 24C56 33 50 42 32 54Z"/>',
}


def svg(inner):
    return f'<svg viewBox="0 0 64 64" aria-hidden="true">{inner}</svg>'


def emblem_html(inner):
    return f'<div class="hero-emblem" aria-hidden="true">{svg(inner)}</div>'
