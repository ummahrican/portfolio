"""
SEO utilities for meta tags, structured data, and sitemap generation.
"""

import json
from datetime import datetime
from typing import Optional
from fasthtml.common import Meta, Link, Script

from app.config import SITE, SEO


def meta_tags(
    title: str,
    description: str,
    url: str,
    image: Optional[str] = None,
    article: bool = False,
    published_time: Optional[str] = None,
    modified_time: Optional[str] = None,
    tags: Optional[list[str]] = None,
    author: Optional[str] = None,
) -> list:
    """
    Generate comprehensive SEO meta tags.

    Args:
        title: Page title
        description: Page description (max 160 chars recommended)
        url: Canonical URL
        image: OpenGraph image URL
        article: Whether this is an article (vs website)
        published_time: ISO date for articles
        modified_time: ISO date for articles
        tags: Article tags/keywords
        author: Article author
    """
    full_title = f"{title} | {SITE.name}" if title != SITE.name else title
    og_image = image or f"{SITE.base_url}{SEO.og_image}"
    canonical = url if url.startswith("http") else f"{SITE.base_url}{url}"

    metas = [
        # Basic meta
        Meta(charset="utf-8"),
        Meta(name="viewport", content="width=device-width, initial-scale=1"),
        Meta(name="description", content=description[:160]),
        Meta(name="author", content=author or SITE.author),
        Meta(name="robots", content="index, follow, max-image-preview:large"),
        # Canonical
        Link(rel="canonical", href=canonical),
        # OpenGraph
        Meta(property="og:type", content="article" if article else SEO.og_type),
        Meta(property="og:site_name", content=SITE.name),
        Meta(property="og:title", content=full_title),
        Meta(property="og:description", content=description[:200]),
        Meta(property="og:url", content=canonical),
        Meta(property="og:image", content=og_image),
        Meta(property="og:image:width", content=str(SEO.og_image_width)),
        Meta(property="og:image:height", content=str(SEO.og_image_height)),
        Meta(property="og:locale", content=SITE.locale),
        # Twitter Card
        Meta(name="twitter:card", content=SEO.twitter_card),
        Meta(name="twitter:site", content=SITE.twitter_handle),
        Meta(name="twitter:creator", content=SITE.twitter_handle),
        Meta(name="twitter:title", content=full_title),
        Meta(name="twitter:description", content=description[:200]),
        Meta(name="twitter:image", content=og_image),
    ]

    # Article-specific meta
    if article:
        if published_time:
            metas.append(
                Meta(property="article:published_time", content=published_time)
            )
        if modified_time:
            metas.append(Meta(property="article:modified_time", content=modified_time))
        if author:
            metas.append(Meta(property="article:author", content=author))
        if tags:
            for tag in tags:
                metas.append(Meta(property="article:tag", content=tag))

    # GEO targeting
    if SEO.geo_region:
        metas.append(Meta(name="geo.region", content=SEO.geo_region))
    if SEO.geo_placename:
        metas.append(Meta(name="geo.placename", content=SEO.geo_placename))
    if SEO.geo_position:
        metas.append(Meta(name="geo.position", content=SEO.geo_position))
        metas.append(Meta(name="ICBM", content=SEO.geo_position.replace(";", ", ")))

    # Keywords from tags
    if tags:
        metas.append(Meta(name="keywords", content=", ".join(tags)))

    return metas


def structured_data_website() -> Script:
    """Generate JSON-LD for website."""
    data = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE.name,
        "description": SITE.description,
        "url": SITE.base_url,
        "author": {
            "@type": "Person",
            "name": SITE.author,
            "url": SITE.base_url,
        },
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{SITE.base_url}/search?q={{search_term_string}}",
            "query-input": "required name=search_term_string",
        },
    }
    return Script(json.dumps(data), type="application/ld+json")


def structured_data_person() -> Script:
    """Generate JSON-LD for author/person."""
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": SITE.author,
        "url": SITE.base_url,
        "sameAs": [
            f"https://twitter.com/{SITE.twitter_handle.lstrip('@')}",
            SITE.github_url,
            SITE.linkedin_url,
        ],
        "jobTitle": "DevOps Engineer & Entrepreneur",
        "worksFor": {
            "@type": "Organization",
            "name": SITE.company_name,
            "url": SITE.company_url,
        },
    }
    return Script(json.dumps(data), type="application/ld+json")


def structured_data_article(
    title: str,
    description: str,
    url: str,
    published: str,
    modified: Optional[str] = None,
    image: Optional[str] = None,
    tags: Optional[list[str]] = None,
) -> Script:
    """Generate JSON-LD for blog article."""
    data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": description,
        "url": f"{SITE.base_url}{url}",
        "datePublished": published,
        "dateModified": modified or published,
        "author": {
            "@type": "Person",
            "name": SITE.author,
            "url": SITE.base_url,
        },
        "publisher": {
            "@type": "Person",
            "name": SITE.author,
            "url": SITE.base_url,
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"{SITE.base_url}{url}",
        },
    }

    if image:
        data["image"] = image if image.startswith("http") else f"{SITE.base_url}{image}"

    if tags:
        data["keywords"] = ", ".join(tags)

    return Script(json.dumps(data), type="application/ld+json")


def structured_data_breadcrumb(items: list[tuple[str, str]]) -> Script:
    """
    Generate JSON-LD breadcrumb.

    Args:
        items: List of (name, url) tuples
    """
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": url if url.startswith("http") else f"{SITE.base_url}{url}",
            }
            for i, (name, url) in enumerate(items)
        ],
    }
    return Script(json.dumps(data), type="application/ld+json")


def structured_data_faq(faqs: list[dict]) -> Script:
    """
    Generate JSON-LD for FAQ page schema.

    This is critical for GEO (Generative Engine Optimization) as AI search
    engines heavily weight FAQ structured data when generating answers.

    Args:
        faqs: List of {"question": "...", "answer": "..."} dicts
    """
    if not faqs:
        return None

    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {"@type": "Answer", "text": faq["answer"]},
            }
            for faq in faqs
            if "question" in faq and "answer" in faq
        ],
    }
    return Script(json.dumps(data), type="application/ld+json")


def preconnect_hints() -> list:
    """Generate resource hints for faster loading."""
    if not SEO.enable_preconnect:
        return []

    hints = []
    for domain in SEO.preconnect_domains:
        hints.append(Link(rel="preconnect", href=domain))
        if "fonts.gstatic.com" in domain:
            hints.append(Link(rel="preconnect", href=domain, crossorigin=True))

    return hints


def generate_sitemap(posts: list, portfolio: list, projects: list) -> str:
    """
    Generate XML sitemap.

    Returns XML string for sitemap.xml
    """
    urls = []

    # Static pages
    static_pages = [
        ("/", "1.0", "weekly"),
        ("/blog", "0.9", "daily"),
        ("/portfolio", "0.8", "monthly"),
        ("/projects", "0.8", "weekly"),
        ("/about", "0.7", "monthly"),
    ]

    for path, priority, changefreq in static_pages:
        urls.append(
            f"""  <url>
    <loc>{SITE.base_url}{path}</loc>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""
        )

    # Blog posts
    for post in posts:
        urls.append(
            f"""  <url>
    <loc>{SITE.base_url}/blog/{post["slug"]}</loc>
    <lastmod>{post.get("modified", post["date"])}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>"""
        )

    # Portfolio items
    for item in portfolio:
        if item.get("slug"):
            urls.append(
                f"""  <url>
    <loc>{SITE.base_url}/portfolio/{item["slug"]}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>"""
            )

    # Projects
    for project in projects:
        if project.get("slug"):
            urls.append(
                f"""  <url>
    <loc>{SITE.base_url}/projects/{project["slug"]}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>"""
            )

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""

    return sitemap


def generate_robots_txt() -> str:
    """Generate robots.txt content."""
    return f"""User-agent: *
Allow: /

# Sitemap
Sitemap: {SITE.base_url}/sitemap.xml

# Crawl-delay for polite bots
Crawl-delay: 1
"""
