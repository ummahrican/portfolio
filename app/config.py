"""
Site configuration and SEO settings.
Update these values to customize your site.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SiteConfig:
    """Core site configuration."""

    name: str = "Ummahrican"
    tagline: str = "DevOps Engineer & Entrepreneur"
    description: str = (
        "Technical deep-dives on Kubernetes, Terraform, Docker, and cloud infrastructure. "
        "7+ years building resilient systems at Apple & Capital One."
    )
    base_url: str = "https://ummahrican.com"
    author: str = "Ahmed"
    author_email: str = "hello@ummahrican.com"
    language: str = "en"
    locale: str = "en_US"

    # Social links
    twitter_handle: str = "@ummahrican"
    github_url: str = "https://github.com/ummahrican"
    linkedin_url: str = "https://linkedin.com/in/ummahrican"

    # Business
    company_name: str = "Seen Web Developers"
    company_url: str = "https://seenwebdev.com"

    # Content settings
    posts_per_page: int = 10
    featured_posts_home: int = 2
    recent_posts_home: int = 4
    portfolio_items_home: int = 3
    projects_home: int = 3


@dataclass
class SEOConfig:
    """SEO and meta tag configuration."""

    # OpenGraph defaults
    og_type: str = "website"
    og_image: str = "/static/og-image.png"
    og_image_width: int = 1200
    og_image_height: int = 630

    # Twitter Card
    twitter_card: str = "summary_large_image"

    # Structured Data
    schema_type: str = "Blog"

    # GEO targeting (optional - set to target specific regions)
    geo_region: Optional[str] = "US"
    geo_placename: Optional[str] = None
    geo_position: Optional[str] = None  # "latitude;longitude"

    # Performance
    enable_preconnect: bool = True
    preconnect_domains: list = field(
        default_factory=lambda: [
            "https://fonts.googleapis.com",
            "https://fonts.gstatic.com",
            "https://cdn.jsdelivr.net",
        ]
    )


@dataclass
class ThemeColors:
    """Mediterranean color palette using OKLCH."""

    terracotta: str = "0.55 0.15 35"
    teal: str = "0.55 0.12 195"
    saffron: str = "0.75 0.15 85"
    deep_blue: str = "0.35 0.08 250"
    olive: str = "0.50 0.10 120"


# Global instances
SITE = SiteConfig()
SEO = SEOConfig()
COLORS = ThemeColors()

# Navigation items
NAV_ITEMS = [
    {"label": "Blog", "href": "/blog"},
    {"label": "Portfolio", "href": "/portfolio"},
    {"label": "Projects", "href": "/projects"},
    {"label": "About", "href": "/about"},
]

# Footer navigation
FOOTER_NAV = {
    "navigation": [
        {"label": "Blog", "href": "/blog"},
        {"label": "Portfolio", "href": "/portfolio"},
        {"label": "Projects", "href": "/projects"},
        {"label": "About", "href": "/about"},
    ],
    "work_with_me": [
        {"label": "Sponsorships", "href": "/sponsorships"},
        {"label": "Consulting", "href": "/consulting"},
        {"label": "Seen Web Dev", "href": SITE.company_url},
    ],
}
