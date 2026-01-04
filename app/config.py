"""
Site configuration.
"""

from dataclasses import dataclass


@dataclass
class SiteConfig:
    name: str = "Ummahrican"
    tagline: str = "DevOps Engineer & Entrepreneur"
    description: str = "Technical deep-dives on Kubernetes, Terraform, and cloud infrastructure."
    base_url: str = "https://ummahrican.com"
    author: str = "Ahmed"
    author_email: str = "hello@ummahrican.com"
    twitter_handle: str = "@ummahrican"
    github_url: str = "https://github.com/ummahrican"
    linkedin_url: str = "https://linkedin.com/in/ummahrican"
    company_name: str = "Seen Web Developers"
    company_url: str = "https://seenwebdev.com"


SITE = SiteConfig()

NAV_ITEMS = [
    {"label": "Blog", "href": "/blog"},
    {"label": "Portfolio", "href": "/portfolio"},
    {"label": "Projects", "href": "/projects"},
    {"label": "About", "href": "/about"},
]

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
