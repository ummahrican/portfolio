"""
Portfolio routes: listing and individual project pages.
"""

from fasthtml.common import (
    Section,
    Div,
    Header,
    Span,
    H1,
    P,
    Article,
    NotStr,
    Aside,
    H3,
    Dl,
    Dt,
    Dd,
    A,
    Footer,
)

from app.config import SITE
from app.components import PortfolioCard, SectionHeader, Pagination, EmptyState, TagList
from app.components.layout import Page, ArticlePage
from app.data import get_all_portfolio, get_portfolio_item_by_slug


def PortfolioListPage(items: list, page: int, total_pages: int):
    """Render the portfolio listing page."""
    return Page(
        Section(
            Div(
                SectionHeader(
                    "Portfolio",
                    "A collection of professional projects, client work, and technical achievements.",
                    accent="secondary",
                ),
                Div(
                    *[PortfolioCard(item) for item in items],
                    cls="grid md:grid-cols-2 lg:grid-cols-3 gap-6",
                )
                if items
                else EmptyState(
                    "No portfolio items yet",
                    "Projects will be added soon!",
                    "Go Home",
                    "/",
                ),
                Pagination(page, total_pages, "/portfolio"),
                cls="max-w-6xl mx-auto px-6",
            ),
            cls="py-16",
        ),
        title="Portfolio",
        description=f"View {SITE.author}'s portfolio of DevOps projects, healthcare technology solutions, and professional work.",
        url="/portfolio",
    )


def PortfolioItemPage(item: dict):
    """Render an individual portfolio item page."""
    breadcrumb = [
        ("Home", "/"),
        ("Portfolio", "/portfolio"),
        (item["title"], f"/portfolio/{item['slug']}"),
    ]

    return ArticlePage(
        Article(
            Header(
                Span(item.get("type", "Project"), cls="badge badge-outline mb-4"),
                H1(
                    item["title"],
                    cls="text-4xl md:text-5xl font-bold mb-4 font-display",
                ),
                P(
                    item.get("description", ""),
                    cls="text-xl text-muted-foreground mb-6",
                ),
                TagList(item.get("tech", [])),
                Div(cls="divider-gradient w-24 my-8"),
                cls="mb-8",
            ),
            # Content
            Div(
                NotStr(item.get("content", "")),
                cls="prose prose-lg max-w-none",
            )
            if item.get("content")
            else None,
            # Project details
            Aside(
                H3("Project Details", cls="text-lg font-semibold mb-4"),
                Dl(
                    Div(
                        Dt("Type", cls="text-sm text-muted-foreground"),
                        Dd(item.get("type", "Project"), cls="font-medium"),
                        cls="mb-3",
                    ),
                    Div(
                        Dt("Year", cls="text-sm text-muted-foreground"),
                        Dd(item.get("year", "2024"), cls="font-medium"),
                        cls="mb-3",
                    )
                    if item.get("year")
                    else None,
                    Div(
                        Dt("Client", cls="text-sm text-muted-foreground"),
                        Dd(item.get("client", "Personal"), cls="font-medium"),
                        cls="mb-3",
                    )
                    if item.get("client")
                    else None,
                    Div(
                        Dt("Link", cls="text-sm text-muted-foreground"),
                        Dd(
                            A(
                                item.get("link", "#"),
                                href=item.get("link", "#"),
                                target="_blank",
                                cls="text-primary hover:underline",
                            ),
                            cls="font-medium",
                        ),
                    )
                    if item.get("link") and item.get("link") != "#"
                    else None,
                ),
                cls="card p-6 my-8",
            ),
            # Navigation
            Footer(
                A("← Back to Portfolio", href="/portfolio", cls="btn btn-outline"),
                cls="mt-8",
            ),
        ),
        title=item["title"],
        description=item.get("description", "")[:160],
        url=f"/portfolio/{item['slug']}",
        breadcrumb_items=breadcrumb,
    )


def NotFoundPage():
    """Portfolio item not found page."""
    return Page(
        Div(
            H1("Project Not Found", cls="text-4xl font-bold font-display mb-4"),
            P(
                "The portfolio item you're looking for doesn't exist.",
                cls="text-muted-foreground mb-6",
            ),
            A("← Back to Portfolio", href="/portfolio", cls="btn btn-primary"),
            cls="text-center py-20 px-6 max-w-xl mx-auto",
        ),
        title="Project Not Found",
        description="The requested portfolio item could not be found.",
        url="/portfolio/not-found",
    )


def register_routes(app, rt):
    """Register portfolio routes."""

    @rt("/portfolio")
    def get(page: int = 1):
        all_items = get_all_portfolio()
        per_page = 9
        total_pages = max(1, (len(all_items) + per_page - 1) // per_page)
        page = max(1, min(page, total_pages))

        start = (page - 1) * per_page
        end = start + per_page
        items = all_items[start:end]

        return PortfolioListPage(items, page, total_pages)

    @rt("/portfolio/{slug}")
    def get(slug: str):
        item = get_portfolio_item_by_slug(slug)
        if not item:
            return NotFoundPage()
        return PortfolioItemPage(item)
