"""
Shared layout templates.
- Page: base wrapper with nav/footer
- ListPage: renders any content collection
- DetailPage: renders any single content item
"""

from fasthtml.common import (
    Html,
    Head,
    Title,
    Body,
    Main,
    Header,
    Footer,
    Nav,
    Section,
    Article,
    Div,
    A,
    H1,
    H2,
    H3,
    P,
    Span,
    NotStr,
    Script,
    Meta,
    Link,
    Style,
)
from app.config import SITE, NAV_ITEMS, FOOTER_NAV


def get_headers():
    """CSS/JS headers."""
    return (
        Script(
            src="https://cdn.tailwindcss.com",
        ),
        Link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/basecoat-css@0.3.9/dist/basecoat.cdn.min.css",
        ),
        Script(
            src="https://cdn.jsdelivr.net/npm/basecoat-css@0.3.9/dist/js/all.min.js",
            defer=True,
        ),
    )


def Navbar():
    """Site navigation."""
    return Header(
        Nav(
            A(
                Span("✦ ", cls="text-[oklch(0.75_0.15_85)]"),
                Span(SITE.name, cls="font-bold"),
                href="/",
                cls="text-xl text-white",
            ),
            Div(
                *[
                    A(
                        item["label"],
                        href=item["href"],
                        cls="text-white/80 hover:text-white px-4 py-2",
                    )
                    for item in NAV_ITEMS
                ],
                cls="hidden md:flex gap-2",
            ),
            cls="flex justify-between items-center max-w-6xl mx-auto px-6 py-4",
        ),
        cls="bg-[oklch(0.35_0.08_250)] sticky top-0 z-50",
    )


def SiteFooter():
    """Site footer."""
    return Footer(
        Div(cls="footer-bar"),
        Div(
            Div(
                Div(
                    A(
                        Span("✦ ", cls="text-accent"),
                        Span(SITE.name),
                        href="/",
                        cls="text-xl text-white mb-4 block font-bold",
                    ),
                    P(SITE.tagline, cls="text-white/60 text-sm"),
                ),
                Div(
                    H3("Navigation", cls="text-white font-semibold mb-4"),
                    *[
                        A(
                            item["label"],
                            href=item["href"],
                            cls="text-white/60 hover:text-white block mb-2 text-sm",
                        )
                        for item in FOOTER_NAV["navigation"]
                    ],
                ),
                Div(
                    H3("Work With Me", cls="text-white font-semibold mb-4"),
                    *[
                        A(
                            item["label"],
                            href=item["href"],
                            cls="text-white/60 hover:text-white block mb-2 text-sm",
                        )
                        for item in FOOTER_NAV["work_with_me"]
                    ],
                ),
                cls="grid md:grid-cols-3 gap-8 py-12 px-6 max-w-6xl mx-auto",
            ),
            Div(
                P(f"© {SITE.author}", cls="text-white/40 text-sm"),
                cls="border-t border-white/10 py-6 px-6 text-center",
            ),
        ),
        cls="bg-[oklch(0.18_0.04_250)]",
    )


def Page(*children, title: str = SITE.name, description: str = SITE.description):
    """Base page wrapper."""
    full_title = f"{title} | {SITE.name}" if title != SITE.name else title
    from app import CUSTOM_CSS, TAILWIND_CONFIG

    return Html(
        Head(
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Title(full_title),
            Meta(name="description", content=description[:160]),
            *get_headers(),
            Script(TAILWIND_CONFIG),
            Style(CUSTOM_CSS),
        ),
        Body(
            Navbar(),
            Main(*children),
            SiteFooter(),
            Script("if(window.lucide)lucide.createIcons();"),
            cls="bg-background text-foreground min-h-screen",
        ),
        lang="en",
    )


def ContentCard(item: dict, base_url: str):
    """Shared card component for list pages."""
    return Article(
        A(
            Div(
                Div(
                    *[
                        Span(tag, cls="badge badge-outline text-xs")
                        for tag in (item.get("tags") or [])[:3]
                    ],
                    cls="flex flex-wrap gap-1 mb-2",
                )
                if item.get("tags")
                else None,
                H3(
                    item["title"],
                    cls="text-lg font-semibold mb-2 group-hover:text-primary",
                ),
                P(
                    item.get("summary", "")[:150],
                    cls="text-muted-foreground text-sm mb-3",
                ),
                Span(item.get("date", ""), cls="text-xs text-muted-foreground")
                if item.get("date")
                else None,
                cls="p-4",
            ),
            href=f"{base_url}/{item['slug']}",
            cls="group block",
        ),
        cls="card card-hover",
    )


def ListPage(items: list, title: str, base_url: str, description: str = ""):
    """
    Shared list template for blog, portfolio, projects.
    Renders title, summary, date sorted by date desc.
    """
    return Page(
        Section(
            Div(
                H1(title, cls="text-3xl font-bold font-display mb-8"),
                Div(
                    *[ContentCard(item, base_url) for item in items],
                    cls="grid md:grid-cols-2 lg:grid-cols-3 gap-6",
                )
                if items
                else P("No content yet.", cls="text-muted-foreground"),
                cls="max-w-6xl mx-auto px-6",
            ),
            cls="py-16",
        ),
        title=title,
        description=description or f"Browse {title.lower()} on {SITE.name}",
    )


def DetailPage(item: dict, back_url: str, back_label: str):
    """
    Shared detail template for any content type.
    Renders full markdown content with title, date, tags.
    """
    return Page(
        Section(
            Div(
                A(
                    f"← {back_label}",
                    href=back_url,
                    cls="text-muted-foreground hover:text-primary text-sm mb-6 inline-block",
                ),
                Article(
                    Header(
                        Div(
                            *[
                                Span(tag, cls="badge badge-outline")
                                for tag in (item.get("tags") or [])
                            ],
                            cls="flex flex-wrap gap-2 mb-4",
                        )
                        if item.get("tags")
                        else None,
                        H1(item["title"], cls="text-4xl font-bold font-display mb-4"),
                        P(item.get("date", ""), cls="text-muted-foreground")
                        if item.get("date")
                        else None,
                        Div(cls="divider-gradient w-24 my-8"),
                    ),
                    Div(
                        NotStr(item.get("content", "")), cls="prose prose-lg max-w-none"
                    ),
                ),
                cls="max-w-4xl mx-auto px-6",
            ),
            cls="py-16",
        ),
        title=item["title"],
        description=item.get("summary", item["title"]),
    )


def NotFoundPage(title: str, message: str, back_url: str, back_label: str):
    """Shared 404 page."""
    return Page(
        Div(
            H1(title, cls="text-4xl font-bold font-display mb-4"),
            P(message, cls="text-muted-foreground mb-6"),
            A(f"← {back_label}", href=back_url, cls="btn btn-primary"),
            cls="text-center py-20 px-6 max-w-xl mx-auto",
        ),
        title=title,
    )
