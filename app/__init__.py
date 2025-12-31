"""
Main application initialization.
"""

from fasthtml.common import fast_app, Script, Link, Style

from app.config import SITE
from app.seo import preconnect_hints


# Tailwind config for Basecoat integration
TAILWIND_CONFIG = """
tailwind.config = {
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                background: 'oklch(var(--background))',
                foreground: 'oklch(var(--foreground))',
                card: 'oklch(var(--card))',
                'card-foreground': 'oklch(var(--card-foreground))',
                primary: 'oklch(var(--primary))',
                'primary-foreground': 'oklch(var(--primary-foreground))',
                secondary: 'oklch(var(--secondary))',
                'secondary-foreground': 'oklch(var(--secondary-foreground))',
                muted: 'oklch(var(--muted))',
                'muted-foreground': 'oklch(var(--muted-foreground))',
                accent: 'oklch(var(--accent))',
                'accent-foreground': 'oklch(var(--accent-foreground))',
                destructive: 'oklch(var(--destructive))',
                border: 'oklch(var(--border))',
                ring: 'oklch(var(--ring))',
            },
            borderRadius: {
                sm: 'calc(var(--radius) - 4px)',
                md: 'calc(var(--radius) - 2px)',
                lg: 'var(--radius)',
                xl: 'calc(var(--radius) + 4px)',
            }
        }
    }
}
"""

# Custom Mediterranean theme CSS
CUSTOM_CSS = """
:root {
    /* Mediterranean color palette using oklch */
    --terracotta: 0.55 0.15 35;
    --teal: 0.55 0.12 195;
    --saffron: 0.75 0.15 85;
    --deep-blue: 0.35 0.08 250;
    --olive: 0.50 0.10 120;
    
    /* Override Basecoat defaults with Mediterranean theme */
    --background: 0.98 0.01 90;
    --foreground: 0.25 0.05 250;
    --card: 1 0 0;
    --card-foreground: 0.25 0.05 250;
    --primary: 0.55 0.15 35;
    --primary-foreground: 0.98 0 0;
    --secondary: 0.55 0.12 195;
    --secondary-foreground: 0.98 0 0;
    --muted: 0.95 0.01 90;
    --muted-foreground: 0.50 0.02 250;
    --accent: 0.75 0.15 85;
    --accent-foreground: 0.25 0.05 250;
    --destructive: 0.55 0.2 25;
    --border: 0.90 0.02 90;
    --ring: 0.55 0.15 35;
    --radius: 0.625rem;
}

.dark {
    --background: 0.18 0.04 250;
    --foreground: 0.95 0.01 90;
    --card: 0.22 0.04 250;
    --card-foreground: 0.95 0.01 90;
    --primary: 0.70 0.12 35;
    --primary-foreground: 0.15 0.02 250;
    --secondary: 0.65 0.10 195;
    --secondary-foreground: 0.15 0.02 250;
    --muted: 0.28 0.03 250;
    --muted-foreground: 0.65 0.02 90;
    --accent: 0.70 0.12 85;
    --accent-foreground: 0.18 0.04 250;
    --border: 0.32 0.03 250;
    --ring: 0.70 0.12 35;
}

body {
    font-family: 'Inter', system-ui, sans-serif;
}

/* Hero pattern */
.hero-pattern {
    background: linear-gradient(135deg, oklch(0.35 0.08 250) 0%, oklch(0.45 0.10 195) 100%);
    position: relative;
}

.hero-pattern::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image: 
        radial-gradient(circle at 20% 50%, oklch(0.55 0.15 35 / 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 50%, oklch(0.55 0.12 195 / 0.1) 0%, transparent 50%);
}

/* Decorative divider */
.divider-gradient {
    height: 4px;
    background: linear-gradient(90deg, 
        transparent 0%, 
        oklch(0.55 0.15 35) 20%, 
        oklch(0.75 0.15 85) 50%, 
        oklch(0.55 0.12 195) 80%, 
        transparent 100%
    );
    border-radius: 2px;
}

/* Card hover effect */
.card-hover {
    transition: all 0.3s ease;
}
.card-hover:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px oklch(0.35 0.08 250 / 0.15);
}

/* Custom badge colors */
.badge-terracotta {
    background: oklch(0.55 0.15 35);
    color: white;
}
.badge-teal {
    background: oklch(0.55 0.12 195);
    color: white;
}
.badge-saffron {
    background: oklch(0.75 0.15 85);
    color: oklch(0.25 0.05 250);
}
.badge-olive {
    background: oklch(0.50 0.10 120);
    color: white;
}

/* Playfair Display for headings */
.font-display {
    font-family: 'Playfair Display', serif;
}

/* Footer gradient bar */
.footer-bar {
    height: 4px;
    background: linear-gradient(90deg, 
        oklch(0.55 0.15 35), 
        oklch(0.75 0.15 85), 
        oklch(0.55 0.12 195)
    );
}

/* Prose styling for blog content */
.prose {
    color: oklch(var(--foreground));
    max-width: 65ch;
}

.prose h1, .prose h2, .prose h3, .prose h4 {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    margin-top: 2em;
    margin-bottom: 0.5em;
}

.prose h1 { font-size: 2.25rem; }
.prose h2 { font-size: 1.875rem; }
.prose h3 { font-size: 1.5rem; }
.prose h4 { font-size: 1.25rem; }

.prose p {
    margin-bottom: 1.25em;
    line-height: 1.75;
}

.prose a {
    color: oklch(var(--primary));
    text-decoration: underline;
}

.prose a:hover {
    color: oklch(var(--secondary));
}

.prose code {
    background: oklch(var(--muted));
    padding: 0.125rem 0.375rem;
    border-radius: 0.25rem;
    font-size: 0.875em;
}

.prose pre {
    background: oklch(0.18 0.04 250);
    color: oklch(0.95 0.01 90);
    padding: 1rem;
    border-radius: 0.5rem;
    overflow-x: auto;
    margin: 1.5em 0;
}

.prose pre code {
    background: transparent;
    padding: 0;
}

.prose blockquote {
    border-left: 4px solid oklch(var(--primary));
    padding-left: 1rem;
    margin: 1.5em 0;
    font-style: italic;
    color: oklch(var(--muted-foreground));
}

.prose ul, .prose ol {
    margin: 1em 0;
    padding-left: 1.5em;
}

.prose li {
    margin-bottom: 0.5em;
}

.prose img {
    border-radius: 0.5rem;
    margin: 1.5em 0;
}

.prose table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5em 0;
}

.prose th, .prose td {
    border: 1px solid oklch(var(--border));
    padding: 0.5rem 1rem;
    text-align: left;
}

.prose th {
    background: oklch(var(--muted));
    font-weight: 600;
}

/* Code highlighting */
.highlight {
    background: oklch(0.18 0.04 250) !important;
    border-radius: 0.5rem;
    margin: 1.5em 0;
}

/* TOC anchor */
.toc-anchor {
    opacity: 0;
    margin-left: 0.5rem;
    color: oklch(var(--muted-foreground));
}

.prose h1:hover .toc-anchor,
.prose h2:hover .toc-anchor,
.prose h3:hover .toc-anchor {
    opacity: 1;
}

/* Screen reader only */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}
"""


def create_headers() -> tuple:
    """Create all header elements for the app."""
    return (
        # Preconnect hints for performance
        *preconnect_hints(),
        # Tailwind CSS CDN
        Script(src="https://cdn.tailwindcss.com"),
        Script(TAILWIND_CONFIG),
        # BasecoatUI CSS and JS
        Link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/basecoat-css@0.3.9/dist/basecoat.cdn.min.css",
        ),
        Script(
            src="https://cdn.jsdelivr.net/npm/basecoat-css@0.3.9/dist/js/all.min.js",
            defer=True,
        ),
        # Google Fonts
        Link(
            rel="stylesheet",
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap",
        ),
        # Lucide icons
        Script(src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"),
        # RSS feed link
        Link(
            rel="alternate",
            type="application/rss+xml",
            title=f"{SITE.name} RSS",
            href="/feed.xml",
        ),
        Link(
            rel="alternate",
            type="application/atom+xml",
            title=f"{SITE.name} Atom",
            href="/feed.atom",
        ),
        # Favicon (placeholder - add your own)
        Link(rel="icon", type="image/png", href="/static/favicon.png"),
        # Custom styles
        Style(CUSTOM_CSS),
    )


def create_app():
    """Create and configure the FastHTML application."""
    from app.routes import register_all_routes

    hdrs = create_headers()
    application, rt = fast_app(hdrs=hdrs, pico=False)

    # Register all routes
    register_all_routes(application, rt)

    return application


# Module-level app instance for uvicorn import ("app:app")
app = create_app()
