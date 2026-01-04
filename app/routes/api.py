"""
Utility routes: sitemap, robots.txt, RSS, health check.
"""

from datetime import datetime
from starlette.responses import Response
from starlette.routing import Route
from app.config import SITE
from app.data import get_posts, get_portfolio, get_projects


def generate_sitemap() -> str:
    """Generate XML sitemap."""
    urls = []
    
    # Static pages
    for path in ["/", "/blog", "/portfolio", "/projects", "/about"]:
        urls.append(f"  <url><loc>{SITE.base_url}{path}</loc></url>")
    
    # Content pages
    for post in get_posts():
        urls.append(f"  <url><loc>{SITE.base_url}/blog/{post['slug']}</loc></url>")
    for item in get_portfolio():
        urls.append(f"  <url><loc>{SITE.base_url}/portfolio/{item['slug']}</loc></url>")
    for project in get_projects():
        urls.append(f"  <url><loc>{SITE.base_url}/projects/{project['slug']}</loc></url>")
    
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""


def generate_rss() -> str:
    """Generate RSS feed."""
    items = []
    for post in get_posts()[:20]:
        items.append(f"""    <item>
      <title><![CDATA[{post["title"]}]]></title>
      <link>{SITE.base_url}/blog/{post["slug"]}</link>
      <description><![CDATA[{post.get("summary", "")}]]></description>
    </item>""")
    
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{SITE.name}</title>
    <link>{SITE.base_url}</link>
    <description>{SITE.description}</description>
{chr(10).join(items)}
  </channel>
</rss>"""


async def sitemap_endpoint(request):
    return Response(generate_sitemap(), media_type="application/xml")

async def robots_endpoint(request):
    content = f"User-agent: *\nAllow: /\nSitemap: {SITE.base_url}/sitemap.xml"
    return Response(content, media_type="text/plain")

async def rss_endpoint(request):
    return Response(generate_rss(), media_type="application/rss+xml")


def register_routes(app, rt):
    # Insert utility routes
    app.routes.insert(0, Route("/sitemap.xml", sitemap_endpoint))
    app.routes.insert(0, Route("/robots.txt", robots_endpoint))
    app.routes.insert(0, Route("/feed.xml", rss_endpoint))

    @rt("/health")
    def get():
        return Response('{"status":"ok"}', media_type="application/json")
