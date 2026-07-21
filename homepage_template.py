"""Homepage template for build_site.py — replaces build_index() return value."""

HOMEPAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bible Study</title>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,400&family=Inter:wght@400;500;600;700&family=Cinzel:wght@400;600;700&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link rel="stylesheet" href="site/style.css?v=12">
    <style>
        body {{ background: #faf5ed !important; }}
        .home-content {{ margin-top: 0; padding: 0; max-width: 100%; margin-left: auto; margin-right: auto; padding-bottom: 60px; background: #faf5ed; }}

        /* Main Hero Section */
        .hero-section {{ position: relative; width: 100%; min-height: 480px; overflow: hidden; display: flex; align-items: center; justify-content: center; }}
        .hero-section img {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; filter: brightness(0.4); }}
        .hero-overlay {{ position: relative; z-index: 1; text-align: center; padding: 40px 28px; max-width: 760px; }}
        .hero-overlay h1 {{ font-family: "Cinzel", serif; font-size: 3.2rem; color: #fff; text-shadow: 2px 2px 12px rgba(0,0,0,0.8); margin-bottom: 12px; letter-spacing: 3px; white-space: nowrap; }}
        .hero-overlay .hero-verse {{ font-family: "Cormorant Garamond", serif; font-size: 1.2rem; color: #f0c865; font-style: italic; text-shadow: 1px 1px 4px rgba(0,0,0,0.6); margin-bottom: 28px; }}
        .hero-overlay .welcome-text {{ font-family: "Cormorant Garamond", serif; font-size: 1.2rem; line-height: 2; color: #f5ebe0; font-style: italic; text-shadow: 1px 1px 6px rgba(0,0,0,0.7); }}

        /* Prayer Section */
        .prayer-section {{ background: linear-gradient(180deg, #1a1410 0%, #2a1f14 15%, #3d2b1f 40%, #4a3828 60%, #6b5040 72%, #a08060 82%, #d4bea0 90%, #f5ebe0 96%, #faf5ed 100%); padding: 52px 32px 80px; text-align: center; }}
        .prayer-text {{ font-family: "Cormorant Garamond", serif; font-size: 1.3rem; line-height: 2.1; color: #f0e4d4; font-style: italic; max-width: 720px; margin: 0 auto; font-weight: 500; }}
        .prayer-label {{ font-family: "Cinzel", serif; font-size: 0.9rem; color: #c9a96e; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 16px; }}
