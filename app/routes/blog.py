"""
Blog routes: listing, individual posts, and tag filtering.
"""

from fasthtml.common import (
    Section,
    Div,
    Aside,
    H1,
    H3,
    H4,
    Header,
    Article,
    Footer,
    Span,
    A,
    P,
    NotStr,
)

from app.config import SITE
from app.components import (
    BlogCardCompact,
    SectionHeader,
    Pagination,
    TagCloud,
    EmptyState,
    TagList,
)
from app.components.layout import Page, ArticlePage
from app.data import (
    get_all_posts,
    get_post_by_slug,
    get_posts_by_tag,
    get_all_tags,
    get_featured_posts,
)


def BlogListPage(
    posts: list, page: int, total_pages: int, title: str = "Blog", subtitle: str = ""
):
    """Render the blog listing page."""
    return Page(
        Section(
            Div(
                SectionHeader(
                    title,
                    subtitle
                    or "Technical deep-dives, lessons learned, and DevOps wisdom.",
                ),
                # Tag cloud
                Aside(
                    H3("Browse by Topic", cls="text-lg font-semibold mb-4"),
                    TagCloud(get_all_tags()[:15]),
                    cls="card p-6 mb-8",
                ),
                # Posts grid
                Div(
                    *[BlogCardCompact(post) for post in posts],
                    cls="grid md:grid-cols-2 lg:grid-cols-3 gap-6",
                )
                if posts
                else EmptyState(
                    "No posts yet",
                    "Check back soon for new content!",
                    "Go Home",
                    "/",
                ),
                Pagination(page, total_pages, "/blog"),
                cls="max-w-6xl mx-auto px-6",
            ),
            cls="py-16",
        ),
        title=title,
        description=f"Browse all {title.lower()} posts on {SITE.name}. DevOps tutorials, infrastructure guides, and tech insights.",
        url="/blog" if title == "Blog" else f"/blog/tag/{title.lower()}",
    )


def BlogPostPage(post: dict):
    """Render an individual blog post."""
    breadcrumb = [
        ("Home", "/"),
        ("Blog", "/blog"),
        (post["title"], f"/blog/{post['slug']}"),
    ]

    return ArticlePage(
        Article(
            # Header
            Header(
                TagList(post.get("tags", [])),
                H1(
                    post["title"],
                    cls="text-4xl md:text-5xl font-bold mt-4 mb-4 font-display",
                ),
                Div(
                    Span(post.get("date", ""), cls="text-muted-foreground"),
                    Span(" · ", cls="text-muted-foreground"),
                    Span(
                        f"📖 {post.get('reading_time', '5 min')}", cls="text-secondary"
                    ),
                    Span(" · ", cls="text-muted-foreground"),
                    Span(
                        f"By {post.get('author', SITE.author)}",
                        cls="text-muted-foreground",
                    ),
                    cls="mb-8",
                ),
                Div(cls="divider-gradient w-24 mb-8"),
                cls="mb-8",
            ),
            # Content
            Div(
                NotStr(post.get("content", "")),
                cls="prose prose-lg max-w-none",
            ),
            # Footer
            Footer(
                Div(cls="divider-gradient w-full my-8"),
                Div(
                    # Tags
                    Div(
                        H4("Topics", cls="text-sm font-semibold mb-2"),
                        TagList(post.get("tags", [])),
                    ),
                    # Share
                    Div(
                        H4("Share", cls="text-sm font-semibold mb-2"),
                        Div(
                            A(
                                "Twitter",
                                href=f"https://twitter.com/intent/tweet?text={post['title']}&url={SITE.base_url}/blog/{post['slug']}",
                                target="_blank",
                                cls="text-muted-foreground hover:text-primary",
                            ),
                            Span(" · ", cls="text-muted-foreground"),
                            A(
                                "LinkedIn",
                                href=f"https://www.linkedin.com/shareArticle?mini=true&url={SITE.base_url}/blog/{post['slug']}&title={post['title']}",
                                target="_blank",
                                cls="text-muted-foreground hover:text-primary",
                            ),
                        ),
                    ),
                    cls="flex justify-between items-start flex-wrap gap-4",
                ),
                # Navigation
                Div(
                    A("← Back to Blog", href="/blog", cls="btn btn-outline"),
                    cls="mt-8",
                ),
            ),
        ),
        title=post["title"],
        description=post.get("excerpt", post.get("description", ""))[:160],
        url=f"/blog/{post['slug']}",
        published_time=post.get("date"),
        modified_time=post.get("modified"),
        tags=post.get("tags", []),
        breadcrumb_items=breadcrumb,
        faqs=post.get("faqs"),  # Pass FAQs for GEO schema
    )


def NotFoundPage():
    """Blog post not found page."""
    return Page(
        Div(
            H1("Post Not Found", cls="text-4xl font-bold font-display mb-4"),
            P(
                "The blog post you're looking for doesn't exist.",
                cls="text-muted-foreground mb-6",
            ),
            A("← Back to Blog", href="/blog", cls="btn btn-primary"),
            cls="text-center py-20 px-6 max-w-xl mx-auto",
        ),
        title="Post Not Found",
        description="The requested blog post could not be found.",
        url="/blog/not-found",
    )


def register_routes(app, rt):
    """Register blog routes."""

    @rt("/blog")
    def get(page: int = 1):
        all_posts = get_all_posts()
        per_page = SITE.posts_per_page
        total_pages = max(1, (len(all_posts) + per_page - 1) // per_page)
        page = max(1, min(page, total_pages))

        start = (page - 1) * per_page
        end = start + per_page
        posts = all_posts[start:end]

        return BlogListPage(posts, page, total_pages)

    @rt("/blog/{slug}")
    def get(slug: str):
        post = get_post_by_slug(slug)
        if not post:
            return NotFoundPage()
        return BlogPostPage(post)

    @rt("/blog/tag/{tag}")
    def get(tag: str, page: int = 1):
        posts = get_posts_by_tag(tag)
        per_page = SITE.posts_per_page
        total_pages = max(1, (len(posts) + per_page - 1) // per_page)
        page = max(1, min(page, total_pages))

        start = (page - 1) * per_page
        end = start + per_page
        paginated_posts = posts[start:end]

        return BlogListPage(
            paginated_posts,
            page,
            total_pages,
            title=f"Posts tagged: {tag.title()}",
            subtitle=f"{len(posts)} post{'s' if len(posts) != 1 else ''} tagged with {tag}",
        )
