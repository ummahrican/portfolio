"""
API and utility routes: sitemap, robots.txt, RSS feed, health checks, and CMS admin.
"""

from datetime import datetime

from starlette.responses import Response
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from app.config import SITE
from app.seo import generate_sitemap, generate_robots_txt
from app.data import get_all_posts, get_all_portfolio, get_all_projects


def generate_rss_feed(posts: list) -> str:
    """Generate RSS 2.0 feed."""
    items = []
    for post in posts[:20]:
        pub_date = post.get("date", "")
        if pub_date:
            try:
                dt = datetime.strptime(pub_date, "%Y-%m-%d")
                pub_date = dt.strftime("%a, %d %b %Y 00:00:00 GMT")
            except ValueError:
                pass

        items.append(
            f"""    <item>
      <title><![CDATA[{post["title"]}]]></title>
      <link>{SITE.base_url}/blog/{post["slug"]}</link>
      <guid isPermaLink="true">{SITE.base_url}/blog/{post["slug"]}</guid>
      <description><![CDATA[{post.get("excerpt", "")}]]></description>
      <pubDate>{pub_date}</pubDate>
      <author>{SITE.author_email} ({SITE.author})</author>
      {chr(10).join(f"      <category>{tag}</category>" for tag in post.get("tags", []))}
    </item>"""
        )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{SITE.name}</title>
    <link>{SITE.base_url}</link>
    <description>{SITE.description}</description>
    <language>{SITE.language}</language>
    <lastBuildDate>{datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")}</lastBuildDate>
    <atom:link href="{SITE.base_url}/feed.xml" rel="self" type="application/rss+xml"/>
    <managingEditor>{SITE.author_email} ({SITE.author})</managingEditor>
    <webMaster>{SITE.author_email} ({SITE.author})</webMaster>
{chr(10).join(items)}
  </channel>
</rss>"""


def generate_atom_feed(posts: list) -> str:
    """Generate Atom feed."""
    entries = []
    for post in posts[:20]:
        updated = post.get("modified", post.get("date", ""))
        if updated and len(updated) == 10:
            updated = f"{updated}T00:00:00Z"

        entries.append(
            f"""  <entry>
    <title><![CDATA[{post["title"]}]]></title>
    <link href="{SITE.base_url}/blog/{post["slug"]}" rel="alternate"/>
    <id>{SITE.base_url}/blog/{post["slug"]}</id>
    <updated>{updated}</updated>
    <summary><![CDATA[{post.get("excerpt", "")}]]></summary>
    <author>
      <name>{SITE.author}</name>
      <email>{SITE.author_email}</email>
    </author>
    {chr(10).join(f'    <category term="{tag}"/>' for tag in post.get("tags", []))}
  </entry>"""
        )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>{SITE.name}</title>
  <link href="{SITE.base_url}" rel="alternate"/>
  <link href="{SITE.base_url}/feed.atom" rel="self"/>
  <id>{SITE.base_url}/</id>
  <updated>{datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}</updated>
  <author>
    <name>{SITE.author}</name>
    <email>{SITE.author_email}</email>
  </author>
{chr(10).join(entries)}
</feed>"""


# Endpoint functions for Starlette routes
async def sitemap_endpoint(request):
    posts = get_all_posts()
    portfolio = get_all_portfolio()
    projects = get_all_projects()
    content = generate_sitemap(posts, portfolio, projects)
    return Response(
        content=content,
        media_type="application/xml",
        headers={"Cache-Control": "public, max-age=3600"},
    )


async def robots_endpoint(request):
    content = generate_robots_txt()
    return Response(
        content=content,
        media_type="text/plain",
        headers={"Cache-Control": "public, max-age=86400"},
    )


async def rss_feed_endpoint(request):
    posts = get_all_posts()
    content = generate_rss_feed(posts)
    return Response(
        content=content,
        media_type="application/rss+xml",
        headers={"Cache-Control": "public, max-age=3600"},
    )


async def atom_feed_endpoint(request):
    posts = get_all_posts()
    content = generate_atom_feed(posts)
    return Response(
        content=content,
        media_type="application/atom+xml",
        headers={"Cache-Control": "public, max-age=3600"},
    )


def register_routes(app, rt):
    """Register API and utility routes, including Decap CMS admin."""

    # Mount Decap CMS admin interface FIRST (highest priority)
    # This serves the static admin files at /admin/*
    app.routes.insert(
        0,
        Mount(
            "/admin",
            app=StaticFiles(directory="static/admin", html=True),
            name="admin",
        ),
    )

    # Insert utility routes at the beginning to take priority over static file handler
    app.routes.insert(0, Route("/sitemap.xml", sitemap_endpoint))
    app.routes.insert(0, Route("/robots.txt", robots_endpoint))
    app.routes.insert(0, Route("/feed.xml", rss_feed_endpoint))
    app.routes.insert(0, Route("/feed.atom", atom_feed_endpoint))

    @rt("/health")
    def get_health():
        """Health check endpoint for load balancers."""
        return Response(
            content='{"status": "healthy"}',
            media_type="application/json",
        )

    @rt("/api/subscribe")
    async def post_subscribe(email: str = ""):
        """Newsletter subscription endpoint (placeholder)."""
        if not email or "@" not in email:
            return Response(
                content='{"error": "Invalid email"}',
                status_code=400,
                media_type="application/json",
            )
        return Response(
            content='{"success": true, "message": "Thanks for subscribing!"}',
            media_type="application/json",
        )
