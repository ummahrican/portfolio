"""
Main application initialization.
Simplified: FastHTML + BasecoatUI only.
"""

from fasthtml.common import fast_app, Script, Link, Style
from app.config import SITE

## TODO: Move to separate file & fix colors to meet accessibility standards
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

CUSTOM_CSS = """
:root {
    --terracotta: 0.55 0.15 35;
    --teal: 0.55 0.12 195;
    --saffron: 0.75 0.15 85;
    --deep-blue: 0.35 0.08 250;
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
body { font-family: 'Inter', system-ui, sans-serif; }
.hero-pattern {
    background: linear-gradient(135deg, oklch(0.35 0.08 250) 0%, oklch(0.45 0.10 195) 100%);
}
.divider-gradient {
    height: 4px;
    background: linear-gradient(90deg, transparent 0%, oklch(0.55 0.15 35) 20%, oklch(0.75 0.15 85) 50%, oklch(0.55 0.12 195) 80%, transparent 100%);
    border-radius: 2px;
}
.card-hover { transition: all 0.3s ease; }
.card-hover:hover { transform: translateY(-4px); box-shadow: 0 12px 40px oklch(0.35 0.08 250 / 0.15); }
.font-display { font-family: 'Playfair Display', serif; }
.footer-bar {
    height: 4px;
    background: linear-gradient(90deg, oklch(0.55 0.15 35), oklch(0.75 0.15 85), oklch(0.55 0.12 195));
}
.prose { color: oklch(var(--foreground)); max-width: 65ch; }
.prose h1, .prose h2, .prose h3, .prose h4 { font-family: 'Playfair Display', serif; font-weight: 700; margin-top: 2em; margin-bottom: 0.5em; }
.prose h1 { font-size: 2.25rem; }
.prose h2 { font-size: 1.875rem; }
.prose h3 { font-size: 1.5rem; }
.prose p { margin-bottom: 1.25em; line-height: 1.75; }
.prose a { color: oklch(var(--primary)); text-decoration: underline; }
.prose code { background: oklch(var(--muted)); padding: 0.125rem 0.375rem; border-radius: 0.25rem; font-size: 0.875em; }
.prose pre { background: oklch(0.18 0.04 250); color: oklch(0.95 0.01 90); padding: 1rem; border-radius: 0.5rem; overflow-x: auto; margin: 1.5em 0; }
.prose pre code { background: transparent; padding: 0; }
.prose blockquote { border-left: 4px solid oklch(var(--primary)); padding-left: 1rem; margin: 1.5em 0; font-style: italic; color: oklch(var(--muted-foreground)); }
.prose ul, .prose ol { margin: 1em 0; padding-left: 1.5em; }
.prose li { margin-bottom: 0.5em; }
.prose table { width: 100%; border-collapse: collapse; margin: 1.5em 0; }
.prose th, .prose td { border: 1px solid oklch(var(--border)); padding: 0.5rem 1rem; text-align: left; }
.prose th { background: oklch(var(--muted)); font-weight: 600; }
"""


def create_headers():
    return (
        Script(src="https://cdn.tailwindcss.com"),
        Script(TAILWIND_CONFIG),
        Link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/basecoat-css@0.3.9/dist/basecoat.cdn.min.css",
        ),
        Script(
            src="https://cdn.jsdelivr.net/npm/basecoat-css@0.3.9/dist/js/all.min.js",
            defer=True,
        ),
        Script(src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"),
        Link(
            rel="alternate",
            type="application/rss+xml",
            title=f"{SITE.name} RSS",
            href="/feed.xml",
        ),
        Style(CUSTOM_CSS),
    )


def create_app():
    from app.routes import register_all_routes

    application, rt = fast_app(hdrs=create_headers(), pico=False)
    register_all_routes(application, rt)
    return application


app = create_app()
