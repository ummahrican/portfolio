"""
Home page route.
Shows featured/recent content with CTAs to full list pages.
"""

from fasthtml.common import (
    Section,
    Div,
    Span,
    H1,
    H2,
    Br,
    P,
    A,
    H4,
    Ul,
    Li,
    Form,
    Input,
    Button,
)

from app.config import SITE
from app.components import BlogCard, PortfolioCard, ProjectCard, SectionHeader
from app.components.layout import Page
from app.data import (
    get_featured_posts,
    get_recent_posts,
    get_all_portfolio,
    get_all_projects,
)


def Hero():
    """Hero section."""
    return Section(
        Div(
            Div(
                Span(
                    "بِسْمِ ٱللَّٰهِ", cls="text-[oklch(0.75_0.15_85)]/80 text-lg mb-4 block"
                ),
                H1(
                    "DevOps Engineer. ",
                    Br(),
                    Span("Entrepreneur. ", cls="text-[oklch(0.75_0.15_85)]"),
                    Br(),
                    "Builder.",
                    cls="text-5xl md:text-6xl font-bold text-white leading-tight mb-6 font-display",
                ),
                P(
                    "7+ years building resilient systems at Apple & Capital One. Now helping healthcare practices grow at ",
                    A(
                        SITE.company_name,
                        href=SITE.company_url,
                        cls="text-[oklch(0.75_0.15_85)] underline hover:text-white transition-colors",
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
                cls="relative z-10 py-20 md:py-32 px-6 max-w-6xl mx-auto",
            ),
        ),
        cls="hero-pattern",
    )


def BlogSection():
    """Blog preview section with featured + recent posts."""
    featured = get_featured_posts(limit=SITE.featured_posts_home)
    recent = get_recent_posts(limit=SITE.recent_posts_home, exclude_featured=True)

    return Section(
        Div(
            SectionHeader(
                "Latest from the Blog",
                "Technical deep-dives, lessons learned, and DevOps wisdom.",
                accent="primary",
            ),
            # Featured posts
            Div(
                *[BlogCard(post, featured=True) for post in featured],
                cls="grid md:grid-cols-2 gap-6 mb-8",
            )
            if featured
            else None,
            # Recent posts
            Div(
                *[BlogCard(post) for post in recent],
                cls="grid md:grid-cols-2 gap-6",
            )
            if recent
            else None,
            # View all CTA
            Div(
                A("View All Posts →", href="/blog", cls="btn btn-outline"),
                cls="text-center mt-8",
            ),
            cls="max-w-6xl mx-auto px-6",
        ),
        id="blog",
        cls="py-20 bg-muted/30",
    )


def PortfolioSection():
    """Portfolio preview section."""
    items = get_all_portfolio()[: SITE.portfolio_items_home]

    if not items:
        return None

    return Section(
        Div(
            SectionHeader(
                "Portfolio",
                "Selected projects and professional work.",
                accent="secondary",
            ),
            Div(
                *[PortfolioCard(item) for item in items],
                cls="grid md:grid-cols-3 gap-6",
            ),
            Div(
                A("View Full Portfolio →", href="/portfolio", cls="btn btn-outline"),
                cls="text-center mt-8",
            ),
            cls="max-w-6xl mx-auto px-6",
        ),
        id="portfolio",
        cls="py-20",
    )


def ProjectsSection():
    """Projects/Micro-SaaS preview section."""
    projects = get_all_projects()[: SITE.projects_home]

    if not projects:
        return None

    return Section(
        Div(
            SectionHeader(
                "Micro-SaaS Projects",
                "Building in public. Small tools, big impact.",
                accent="accent",
            ),
            Div(
                *[ProjectCard(project) for project in projects],
                cls="grid md:grid-cols-3 gap-6",
            ),
            Div(
                A("View All Projects →", href="/projects", cls="btn btn-outline"),
                cls="text-center mt-8",
            ),
            cls="max-w-6xl mx-auto px-6",
        ),
        id="projects",
        cls="py-20 bg-muted/30",
    )


def AboutSection():
    """About preview section."""
    return Section(
        Div(
            Div(
                Div(
                    Span("✦ ", cls="text-primary"),
                    Span("About Me", cls="text-3xl font-bold font-display"),
                    cls="mb-6",
                ),
                P(
                    "I'm a DevOps engineer turned entrepreneur with a passion for building reliable systems. "
                    "After 7+ years at Apple and Capital One, I co-founded ",
                    A(
                        SITE.company_name,
                        href=SITE.company_url,
                        cls="text-primary hover:underline",
                    ),
                    " — a Muslim-owned digital marketing agency specializing in healthcare.",
                    cls="text-lg mb-4",
                ),
                P(
                    "We operate with Islamic business principles, including donating 10% of profits to charity.",
                    cls="text-lg text-muted-foreground mb-6",
                ),
                H4("What I Write About", cls="text-xl font-semibold mb-3"),
                Ul(
                    Li("🐳 Container orchestration & Kubernetes"),
                    Li("🏗️ Infrastructure as Code (Terraform, Pulumi)"),
                    Li("🔒 Security & Compliance"),
                    Li("💰 Cloud cost optimization"),
                    Li("🚀 CI/CD pipelines & DevOps culture"),
                    cls="space-y-2 text-muted-foreground",
                ),
                A("Learn More About Me →", href="/about", cls="btn btn-primary mt-6"),
                cls="md:col-span-2",
            ),
            Div(
                Div(
                    H4("Experience", cls="font-semibold mb-4"),
                    Div(
                        Div(
                            Span("Apple", cls="font-medium"),
                            Span(" — SRE", cls="text-muted-foreground text-sm"),
                            cls="mb-2",
                        ),
                        Div(
                            Span("Capital One", cls="font-medium"),
                            Span(" — DevOps", cls="text-muted-foreground text-sm"),
                            cls="mb-2",
                        ),
                        Div(
                            Span(SITE.company_name, cls="font-medium text-primary"),
                            Span(" — CTO", cls="text-muted-foreground text-sm"),
                        ),
                    ),
                    cls="card p-6 mb-6",
                ),
                Div(
                    H4("Connect", cls="font-semibold mb-4"),
                    A(
                        "GitHub",
                        href=SITE.github_url,
                        cls="block text-muted-foreground hover:text-primary mb-2",
                    ),
                    A(
                        "LinkedIn",
                        href=SITE.linkedin_url,
                        cls="block text-muted-foreground hover:text-primary mb-2",
                    ),
                    A(
                        "Twitter/X",
                        href=f"https://twitter.com/{SITE.twitter_handle.lstrip('@')}",
                        cls="block text-muted-foreground hover:text-primary",
                    ),
                    cls="card p-6",
                ),
            ),
            cls="grid md:grid-cols-3 gap-12 max-w-6xl mx-auto px-6",
        ),
        id="about",
        cls="py-20",
    )


def Newsletter():
    """Newsletter signup section."""
    return Section(
        Div(
            H2("Stay Updated", cls="text-2xl font-bold text-white mb-2 font-display"),
            P(
                "Get DevOps insights delivered to your inbox. No spam.",
                cls="text-white/80 mb-6",
            ),
            Form(
                Div(
                    Input(
                        type="email",
                        name="email",
                        placeholder="your@email.com",
                        required=True,
                        cls="input bg-white/10 border-white/20 text-white placeholder:text-white/50",
                    ),
                    Button("Subscribe", type="submit", cls="btn btn-primary"),
                    cls="flex gap-3 flex-wrap justify-center",
                ),
                action="/api/subscribe",
                method="post",
            ),
            cls="text-center py-16 px-6 max-w-xl mx-auto",
        ),
        cls="bg-[oklch(0.35_0.08_250)]",
    )


def register_routes(app, rt):
    """Register home page routes."""

    @rt("/")
    def get():
        return Page(
            Hero(),
            BlogSection(),
            PortfolioSection(),
            ProjectsSection(),
            AboutSection(),
            Newsletter(),
            title=SITE.name,
            description=SITE.description,
            url="/",
        )
