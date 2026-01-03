"""
Home page route with HTMS streaming for progressive enhancement.
Shows featured/recent content with CTAs to full list pages.
"""

from fasthtml.common import *

from app.config import SITE
from app.components import BlogCard, PortfolioCard, ProjectCard, SectionHeader
from app.components.skeletons import (
    FeaturedSkeleton,
    PostGridSkeleton,
    ErrorFallback,
)
from app.streaming import (
    streaming_page,
    ChunkConfig,
    generate_chunk_id,
)
from app.seo import meta_tags, structured_data_website, structured_data_person
from app.data import (
    get_featured_posts,
    get_recent_posts,
    get_all_portfolio,
    get_all_projects,
)


def render_headers():
    """Render all app headers as HTML string for streaming."""
    from app import create_headers

    headers = create_headers()
    return "".join([str(h) for h in headers])


def Hero():
    """Hero section - renders immediately (no streaming)."""
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


def Navbar():
    """Simple navbar for initial HTML."""
    from app.config import NAV_ITEMS

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
            cls="flex justify-between items-center max-w-6xl mx-auto px-6 py-4",
        ),
        cls="bg-[oklch(0.35_0.08_250)] sticky top-0 z-50",
    )


def SiteFooter():
    """Simple footer for initial HTML."""
    from app.config import FOOTER_NAV

    return Footer(
        Div(cls="footer-bar"),
        Div(
            Div(
                Div(
                    A(
                        Span("✦ ", cls="text-accent"),
                        Span(SITE.name, cls="font-bold"),
                        href="/",
                        cls="text-xl text-white mb-4 block",
                    ),
                    P(SITE.tagline, cls="text-white/60 text-sm"),
                ),
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


def AboutSection():
    """About preview section - renders immediately (no streaming)."""
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


def register_routes(app, rt):
    """Register home page routes with HTMS streaming."""

    @rt("/")
    async def get():
        """
        Homepage with progressive HTML streaming.

        Flow:
        1. Send initial HTML skeleton immediately (FCP <300ms)
        2. Stream featured posts when ready
        3. Stream recent posts when ready
        4. Stream portfolio/projects when ready
        """
        # Generate unique IDs for this request
        featured_id = generate_chunk_id("featured")
        recent_id = generate_chunk_id("recent")
        portfolio_id = generate_chunk_id("portfolio")
        projects_id = generate_chunk_id("projects")

        # Build meta tags and structured data
        title = SITE.name
        description = SITE.description
        url = "/"

        metas = meta_tags(title, description, url)
        meta_html = "".join([str(m) for m in metas])

        structured = [structured_data_website(), structured_data_person()]
        structured_html = "".join([str(s) for s in structured])

        # Get all headers (Tailwind, BasecoatUI, fonts, etc.)
        headers_html = render_headers()

        # Build initial HTML that renders immediately
        initial_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    {meta_html}
    {structured_html}
    {headers_html}
</head>
<body class="bg-background text-foreground min-h-screen">
    {str(Navbar())}
    
    <main>
        {str(Hero())}
        
        <!-- Featured Blog Section (HTMS streaming) -->
        <section class="py-20 bg-muted/30" id="blog">
            <div class="max-w-6xl mx-auto px-6">
                {
            str(
                SectionHeader(
                    "Latest from the Blog",
                    "Technical deep-dives, lessons learned, and DevOps wisdom.",
                    accent="primary",
                )
            )
        }
                <div data-htms-uuid="{featured_id}" class="htms-placeholder">
                    {str(FeaturedSkeleton(2))}
                </div>
                <div class="text-center mt-8">
                    <a href="/blog" class="btn btn-outline">View All Posts →</a>
                </div>
            </div>
        </section>
        
        <!-- Recent Posts Section (HTMS streaming) -->
        <section class="py-20">
            <div class="max-w-6xl mx-auto px-6">
                {
            str(
                SectionHeader(
                    "Recent Posts",
                    "Catch up on the latest tutorials and insights.",
                    accent="secondary",
                )
            )
        }
                <div data-htms-uuid="{recent_id}" class="htms-placeholder">
                    {str(PostGridSkeleton(4))}
                </div>
            </div>
        </section>
        
        <!-- Portfolio Section (HTMS streaming) -->
        <section class="py-20 bg-muted/30" id="portfolio">
            <div class="max-w-6xl mx-auto px-6">
                {
            str(
                SectionHeader(
                    "Portfolio",
                    "Selected projects and professional work.",
                    accent="secondary",
                )
            )
        }
                <div data-htms-uuid="{portfolio_id}" class="htms-placeholder">
                    {str(PostGridSkeleton(3))}
                </div>
                <div class="text-center mt-8">
                    <a href="/portfolio" class="btn btn-outline">View Full Portfolio →</a>
                </div>
            </div>
        </section>
        
        <!-- Projects Section (HTMS streaming) -->
        <section class="py-20" id="projects">
            <div class="max-w-6xl mx-auto px-6">
                {
            str(
                SectionHeader(
                    "Micro-SaaS Projects",
                    "Building in public. Small tools, big impact.",
                    accent="accent",
                )
            )
        }
                <div data-htms-uuid="{projects_id}" class="htms-placeholder">
                    {str(PostGridSkeleton(3))}
                </div>
                <div class="text-center mt-8">
                    <a href="/projects" class="btn btn-outline">View All Projects →</a>
                </div>
            </div>
        </section>
        
        {str(AboutSection())}
        {str(Newsletter())}
    </main>
    
    {str(SiteFooter())}
    
    <script>
        // Initialize Lucide icons when they load
        if (window.lucide) {{
            lucide.createIcons();
        }}
        document.addEventListener('DOMContentLoaded', function() {{
            if (window.lucide) {{
                lucide.createIcons();
            }}
        }});
    </script>
"""

        # Define async data fetchers
        async def fetch_featured():
            """Fetch featured blog posts."""
            posts = get_featured_posts(limit=SITE.featured_posts_home)
            if not posts:
                return str(ErrorFallback("No featured posts yet"))

            cards = Div(
                *[BlogCard(post, featured=True) for post in posts],
                cls="grid md:grid-cols-2 gap-6 mb-8",
            )
            return str(cards)

        async def fetch_recent():
            """Fetch recent blog posts."""
            posts = get_recent_posts(
                limit=SITE.recent_posts_home, exclude_featured=True
            )
            if not posts:
                return str(ErrorFallback("No posts yet"))

            cards = Div(
                *[BlogCard(post) for post in posts], cls="grid md:grid-cols-2 gap-6"
            )
            return str(cards)

        async def fetch_portfolio():
            """Fetch portfolio items."""
            items = get_all_portfolio()[: SITE.portfolio_items_home]
            if not items:
                return str(ErrorFallback("No portfolio items yet"))

            cards = Div(
                *[PortfolioCard(item) for item in items],
                cls="grid md:grid-cols-3 gap-6",
            )
            return str(cards)

        async def fetch_projects():
            """Fetch projects."""
            projects = get_all_projects()[: SITE.projects_home]
            if not projects:
                return str(ErrorFallback("No projects yet"))

            cards = Div(
                *[ProjectCard(project) for project in projects],
                cls="grid md:grid-cols-3 gap-6",
            )
            return str(cards)

        # Configure streaming chunks
        chunks = {
            featured_id: ChunkConfig(
                id=featured_id,
                fetcher=fetch_featured,
                fallback_html=str(ErrorFallback("Couldn't load featured posts")),
                timeout=5.0,
                retries=1,
            ),
            recent_id: ChunkConfig(
                id=recent_id,
                fetcher=fetch_recent,
                fallback_html=str(ErrorFallback("Couldn't load recent posts")),
                timeout=5.0,
                retries=1,
            ),
            portfolio_id: ChunkConfig(
                id=portfolio_id,
                fetcher=fetch_portfolio,
                fallback_html=str(ErrorFallback("Couldn't load portfolio")),
                timeout=5.0,
                retries=1,
            ),
            projects_id: ChunkConfig(
                id=projects_id,
                fetcher=fetch_projects,
                fallback_html=str(ErrorFallback("Couldn't load projects")),
                timeout=5.0,
                retries=1,
            ),
        }

        # Return streaming response
        return streaming_page(initial_html, chunks, close_html="</body></html>")
