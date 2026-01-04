"""
Homepage: statement + featured projects + latest posts.
"""

from fasthtml.common import Section, Div, H1, H2, P, A, Span, Br
from app.config import SITE
from app.components.layout import Page, ContentCard
from app.data import get_posts, get_projects


def Hero():
    """Hero section with statement."""
    return Section(
        Div(
            H1(
                "DevOps Engineer. ",
                Br(),
                Span("Entrepreneur. ", cls="text-[oklch(0.75_0.15_85)]"),
                Br(),
                "Builder.",
                cls="text-5xl md:text-6xl font-bold text-white leading-tight mb-6 font-display",
            ),
            P(
                "Building resilient systems and helping businesses grow at ",
                A(
                    SITE.company_name,
                    href=SITE.company_url,
                    cls="text-[oklch(0.75_0.15_85)] underline hover:text-white",
                ),
                ".",
                cls="text-xl text-white/80 mb-8 max-w-xl",
            ),
            Div(
                A("Read the Blog", href="/blog", cls="btn btn-primary"),
                A(
                    "View Projects",
                    href="/projects",
                    cls="btn btn-outline border-white/30 text-white hover:bg-white/10",
                ),
                cls="flex gap-4 flex-wrap",
            ),
            cls="py-20 md:py-32 px-6 max-w-6xl mx-auto",
        ),
        cls="hero-pattern",
    )


def HomePage():
    """Homepage with hero, featured projects, latest posts."""
    projects = get_projects()[:5]
    posts = get_posts()[:3]

    return Page(
        Hero(),
        # Featured Projects
        Section(
            Div(
                H2("Projects", cls="text-2xl font-bold font-display mb-6"),
                Div(
                    *[ContentCard(p, "/projects") for p in projects],
                    cls="grid md:grid-cols-3 gap-6",
                )
                if projects
                else P("No projects yet.", cls="text-muted-foreground"),
                A("View All Projects →", href="/projects", cls="btn btn-outline mt-8"),
                cls="max-w-6xl mx-auto px-6",
            ),
            cls="py-16",
        ),
        # Latest Posts
        Section(
            Div(
                H2("Latest Posts", cls="text-2xl font-bold font-display mb-6"),
                Div(
                    *[ContentCard(p, "/blog") for p in posts],
                    cls="grid md:grid-cols-3 gap-6",
                )
                if posts
                else P("No posts yet.", cls="text-muted-foreground"),
                A("View All Posts →", href="/blog", cls="btn btn-outline mt-8"),
                cls="max-w-6xl mx-auto px-6",
            ),
            cls="py-16 bg-muted/30",
        ),
        title=SITE.name,
    )


def register_routes(app, rt):
    @rt("/")
    def get():
        return HomePage()
