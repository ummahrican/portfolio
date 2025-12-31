"""
Reusable UI components for the site.
"""

from fasthtml.common import (
    Span,
    Div,
    H3,
    A,
    P,
    Article,
    Nav,
)

# from app.config import SITE, COLORS, NAV_ITEMS, FOOTER_NAV


# Tag color variants
TAG_VARIANTS = {
    "terracotta": "badge-terracotta",
    "teal": "badge-teal",
    "saffron": "badge-saffron",
    "olive": "badge-olive",
}


def Tag(text: str, variant: str = "terracotta"):
    """Render a tag/badge."""
    cls = TAG_VARIANTS.get(variant, "badge")
    return Span(text, cls=f"badge {cls}")


def TagList(tags: list[str]):
    """Render a list of tags with rotating colors."""
    variants = list(TAG_VARIANTS.keys())
    return Div(
        *[Tag(tag, variants[i % len(variants)]) for i, tag in enumerate(tags)],
        cls="flex flex-wrap gap-2",
    )


def StatusBadge(status: str):
    """Render a status badge for projects."""
    status_map = {
        "live": ("● Live", "bg-green-500 text-white"),
        "beta": ("◐ Beta", "badge-saffron"),
        "building": ("◔ Building", "badge-terracotta"),
    }
    text, cls = status_map.get(status, ("○ Unknown", "badge"))
    return Span(text, cls=f"badge {cls}")


def BlogCard(post: dict, featured: bool = False):
    """Render a blog post card."""
    return Article(
        Div(
            TagList(post.get("tags", [])),
            H3(
                A(
                    post["title"],
                    href=f"/blog/{post['slug']}",
                    cls="hover:text-primary transition-colors",
                ),
                cls="text-xl font-semibold mb-2 font-display mt-3",
            ),
            P(post.get("excerpt", ""), cls="text-muted-foreground mb-4"),
            Div(
                Span(post.get("date", ""), cls="text-sm text-muted-foreground"),
                Span(" · ", cls="text-muted-foreground"),
                Span(
                    f"📖 {post.get('reading_time', '5 min')}",
                    cls="text-sm text-secondary",
                ),
                cls="flex items-center",
            ),
            cls="p-6",
        ),
        cls=f"card card-hover {'border-l-4 border-l-primary' if featured else ''}",
    )


def BlogCardCompact(post: dict):
    """Render a compact blog post card for list pages."""
    return Article(
        A(
            Div(
                Div(
                    TagList(post.get("tags", [])[:3]),  # Show max 3 tags
                    cls="mb-2",
                ),
                H3(
                    post["title"],
                    cls="text-lg font-semibold mb-2 group-hover:text-primary transition-colors",
                ),
                P(
                    post.get("excerpt", "")[:120] + "...",
                    cls="text-muted-foreground text-sm mb-3",
                ),
                Div(
                    Span(post.get("date", ""), cls="text-xs text-muted-foreground"),
                    Span(" · ", cls="text-muted-foreground"),
                    Span(
                        post.get("reading_time", "5 min"), cls="text-xs text-secondary"
                    ),
                    cls="flex items-center",
                ),
                cls="p-4",
            ),
            href=f"/blog/{post['slug']}",
            cls="group block",
        ),
        cls="card card-hover",
    )


def PortfolioCard(item: dict):
    """Render a portfolio card."""
    return Article(
        Div(
            Span(item.get("type", "Project"), cls="badge badge-outline mb-3"),
            H3(item["title"], cls="text-xl font-semibold mb-2 font-display"),
            P(item.get("description", ""), cls="text-muted-foreground mb-4"),
            TagList(item.get("tech", [])),
            A(
                "View Project →",
                href=item.get("link", "#"),
                cls="text-primary hover:underline font-medium mt-4 inline-block",
            ),
            cls="p-6",
        ),
        cls="card card-hover",
    )


def ProjectCard(project: dict):
    """Render a project/micro-SaaS card."""
    return Article(
        Div(
            StatusBadge(project.get("status", "building")),
            H3(project["name"], cls="text-xl font-bold mt-4 mb-1 font-display"),
            P(project.get("tagline", ""), cls="text-primary text-sm mb-4"),
            Div(
                Div(
                    Span("MRR", cls="text-xs text-muted-foreground block"),
                    Span(project.get("mrr", "N/A"), cls="font-semibold"),
                ),
                Div(
                    Span("Users", cls="text-xs text-muted-foreground block"),
                    Span(project.get("users", "-"), cls="font-semibold"),
                ),
                cls="grid grid-cols-2 gap-4 pt-4 border-t",
            ),
            cls="p-6",
        ),
        cls="card card-hover border-t-4 border-t-secondary",
    )


def SectionHeader(title: str, subtitle: str = "", accent: str = "primary"):
    """Render a section header with decorative elements."""
    accent_classes = {
        "primary": "text-primary",
        "secondary": "text-secondary",
        "accent": "text-accent",
    }
    return Div(
        Div(
            Span("✦ ", cls=accent_classes.get(accent, "text-primary")),
            Span(title, cls="text-3xl font-bold font-display"),
            P(subtitle, cls="text-muted-foreground mt-2") if subtitle else None,
            cls="text-center mb-8",
        ),
        Div(cls="divider-gradient w-24 mx-auto mb-12"),
    )


def Pagination(current_page: int, total_pages: int, base_url: str):
    """Render pagination controls."""
    if total_pages <= 1:
        return None

    items = []

    # Previous
    if current_page > 1:
        items.append(
            A(
                "← Previous",
                href=f"{base_url}?page={current_page - 1}",
                cls="btn btn-outline",
            )
        )
    else:
        items.append(
            Span("← Previous", cls="btn btn-outline opacity-50 cursor-not-allowed")
        )

    # Page numbers
    for page in range(1, total_pages + 1):
        if page == current_page:
            items.append(Span(str(page), cls="btn btn-primary"))
        else:
            items.append(
                A(str(page), href=f"{base_url}?page={page}", cls="btn btn-outline")
            )

    # Next
    if current_page < total_pages:
        items.append(
            A(
                "Next →",
                href=f"{base_url}?page={current_page + 1}",
                cls="btn btn-outline",
            )
        )
    else:
        items.append(
            Span("Next →", cls="btn btn-outline opacity-50 cursor-not-allowed")
        )

    return Nav(*items, cls="flex justify-center gap-2 mt-12")


def Breadcrumb(items: list[tuple[str, str]]):
    """
    Render breadcrumb navigation.

    Args:
        items: List of (label, url) tuples. Last item is current page.
    """
    parts = []
    for i, (label, url) in enumerate(items):
        if i == len(items) - 1:
            # Current page (no link)
            parts.append(Span(label, cls="text-foreground"))
        else:
            parts.append(
                A(label, href=url, cls="text-muted-foreground hover:text-primary")
            )
            parts.append(Span(" / ", cls="text-muted-foreground mx-2"))

    return Nav(*parts, cls="text-sm mb-6", aria_label="Breadcrumb")


def EmptyState(
    title: str, message: str, action_text: str = None, action_url: str = None
):
    """Render an empty state message."""
    return Div(
        H3(title, cls="text-xl font-semibold mb-2"),
        P(message, cls="text-muted-foreground mb-4"),
        A(action_text, href=action_url, cls="btn btn-primary") if action_text else None,
        cls="text-center py-16",
    )


def TagCloud(tags: list[tuple[str, int]], base_url: str = "/blog/tag"):
    """Render a tag cloud with counts."""
    return Div(
        *[
            A(
                f"{tag} ({count})",
                href=f"{base_url}/{tag}",
                cls="badge badge-outline hover:bg-primary hover:text-primary-foreground transition-colors",
            )
            for tag, count in tags
        ],
        cls="flex flex-wrap gap-2",
    )
