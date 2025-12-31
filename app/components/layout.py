"""
Layout components: Navbar, Footer, and page wrappers.
"""

from fasthtml.common import (
    Header,
    Nav,
    Div,
    A,
    Span,
    Button,
    Footer,
    P,
    H4,
    Title,
    Body,
    Script,
    Main,
)

from app.config import SITE, NAV_ITEMS, FOOTER_NAV
from app.seo import (
    meta_tags,
    structured_data_website,
    structured_data_person,
)


def Navbar():
    """Site navigation header."""
    return Header(
        Nav(
            Div(
                A(
                    Span("✦ ", cls="text-[oklch(0.75_0.15_85)]"),
                    Span(SITE.name, cls="font-bold"),
                    href="/",
                    cls="text-xl text-white flex items-center",
                ),
                cls="flex items-center",
            ),
            # Desktop navigation
            Div(
                *[
                    A(
                        item["label"],
                        href=item["href"],
                        cls="text-white/80 hover:text-white px-4 py-2 transition-colors",
                    )
                    for item in NAV_ITEMS
                ],
                cls="hidden md:flex items-center gap-2",
            ),
            # Mobile menu button
            Button(
                Span(cls="sr-only", _="Menu"),
                Div(
                    Span(cls="block w-5 h-0.5 bg-white mb-1"),
                    Span(cls="block w-5 h-0.5 bg-white mb-1"),
                    Span(cls="block w-5 h-0.5 bg-white"),
                ),
                cls="md:hidden p-2",
                onclick="document.getElementById('mobile-menu').classList.toggle('hidden')",
            ),
            cls="flex justify-between items-center max-w-6xl mx-auto px-6 py-4",
        ),
        # Mobile navigation
        Nav(
            *[
                A(
                    item["label"],
                    href=item["href"],
                    cls="block text-white/80 hover:text-white px-6 py-3 border-b border-white/10",
                )
                for item in NAV_ITEMS
            ],
            id="mobile-menu",
            cls="hidden md:hidden bg-[oklch(0.30_0.08_250)]",
        ),
        cls="bg-[oklch(0.35_0.08_250)] sticky top-0 z-50",
    )


def SiteFooter():
    """Site footer."""
    return Footer(
        Div(cls="footer-bar"),
        Div(
            Div(
                # Brand
                Div(
                    A(
                        Span("✦ ", cls="text-accent"),
                        Span(SITE.name, cls="font-bold"),
                        href="/",
                        cls="text-xl text-white mb-4 block",
                    ),
                    P(SITE.tagline, cls="text-white/60 text-sm"),
                ),
                # Navigation
                Div(
                    H4("Navigation", cls="text-white font-semibold mb-4"),
                    *[
                        A(
                            item["label"],
                            href=item["href"],
                            cls="text-white/60 hover:text-white block mb-2 text-sm",
                        )
                        for item in FOOTER_NAV["navigation"]
                    ],
                ),
                # Work with me
                Div(
                    H4("Work With Me", cls="text-white font-semibold mb-4"),
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
            # Copyright
            Div(
                P(
                    f"© {SITE.author}. Built with ",
                    A(
                        "FastHTML",
                        href="https://fasthtml.dev",
                        cls="text-accent hover:underline",
                    ),
                    " & ",
                    A(
                        "BasecoatUI",
                        href="https://basecoatui.com",
                        cls="text-accent hover:underline",
                    ),
                    ".",
                    cls="text-white/40 text-sm",
                ),
                cls="border-t border-white/10 py-6 px-6 text-center",
            ),
        ),
        cls="bg-[oklch(0.18_0.04_250)]",
    )


def PageHead(
    title: str,
    description: str,
    url: str,
    article: bool = False,
    **seo_kwargs,
):
    """
    Generate the <head> contents with SEO meta tags.

    This should be used within Title() or as part of hdrs.
    """
    metas = meta_tags(title, description, url, article=article, **seo_kwargs)
    return metas


def Page(
    *children,
    title: str = SITE.name,
    description: str = SITE.description,
    url: str = "/",
    article: bool = False,
    include_structured_data: bool = True,
    **seo_kwargs,
):
    """
    Full page wrapper with layout and SEO.

    Usage:
        return Page(
            content_here,
            title="My Page",
            description="Page description",
            url="/my-page"
        )
    """
    structured_data = []
    if include_structured_data:
        structured_data = [structured_data_website(), structured_data_person()]

    full_title = f"{title} | {SITE.name}" if title != SITE.name else title

    return (
        Title(full_title),
        *meta_tags(title, description, url, article=article, **seo_kwargs),
        *structured_data,
        Body(
            Navbar(),
            Main(*children),
            Footer(),
            Script("lucide.createIcons();"),
            cls="bg-background text-foreground min-h-screen",
        ),
    )


def ArticlePage(
    *children,
    title: str,
    description: str,
    url: str,
    published_time: str = None,
    modified_time: str = None,
    tags: list[str] = None,
    breadcrumb_items: list[tuple[str, str]] = None,
    faqs: list[dict] = None,
):
    """
    Article page wrapper with enhanced SEO for blog posts.

    Args:
        faqs: List of {"question": "...", "answer": "..."} for FAQ schema (GEO optimization)
    """
    from app.seo import (
        structured_data_article,
        structured_data_breadcrumb,
        structured_data_faq,
    )
    from app.components import Breadcrumb

    structured_data = [
        structured_data_website(),
        structured_data_article(
            title=title,
            description=description,
            url=url,
            published=published_time,
            modified=modified_time,
            tags=tags,
        ),
    ]

    if breadcrumb_items:
        structured_data.append(structured_data_breadcrumb(breadcrumb_items))

    # Add FAQ schema for GEO (Generative Engine Optimization)
    if faqs:
        faq_schema = structured_data_faq(faqs)
        if faq_schema:
            structured_data.append(faq_schema)

    full_title = f"{title} | {SITE.name}"

    return (
        Title(full_title),
        *meta_tags(
            title,
            description,
            url,
            article=True,
            published_time=published_time,
            modified_time=modified_time,
            tags=tags,
        ),
        *structured_data,
        Body(
            Navbar(),
            Main(
                Div(
                    Breadcrumb(breadcrumb_items) if breadcrumb_items else None,
                    *children,
                    cls="max-w-4xl mx-auto px-6 py-12",
                ),
            ),
            SiteFooter(),
            Script("lucide.createIcons();"),
            cls="bg-background text-foreground min-h-screen",
        ),
    )
