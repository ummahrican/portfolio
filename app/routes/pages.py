"""
Static pages: About, Contact, Sponsorships, etc.
"""

from fasthtml.common import Section, Div, P, A, H2, H3, Span, Ul, Li, Strong, Aside

from app.config import SITE
from app.components import SectionHeader
from app.components.layout import Page


def AboutPage():
    """Full about page."""
    return Page(
        Section(
            Div(
                # Header
                SectionHeader("About Me", "DevOps Engineer & Entrepreneur"),
                # Two column layout
                Div(
                    # Main content
                    Div(
                        # Intro
                        Div(
                            P(
                                "I'm Ahmed, a DevOps engineer turned entrepreneur with over 7 years of "
                                "experience building and scaling infrastructure at companies like Apple and Capital One.",
                                cls="text-lg mb-4",
                            ),
                            P(
                                "Today, I'm the CTO and Co-founder of ",
                                A(
                                    SITE.company_name,
                                    href=SITE.company_url,
                                    cls="text-primary hover:underline",
                                ),
                                ", a Muslim-owned digital marketing agency that specializes in healthcare providers. "
                                "We help medical practices grow their online presence through SEO, website development, "
                                "and HIPAA-compliant custom applications.",
                                cls="text-lg mb-4",
                            ),
                            P(
                                "Our business operates on Islamic principles—we donate 10% of our profits to charity "
                                "and maintain Sharia-compliant practices in all our dealings.",
                                cls="text-lg text-muted-foreground mb-6",
                            ),
                            cls="mb-8",
                        ),
                        # What I do
                        Div(
                            H2("What I Do", cls="text-2xl font-bold font-display mb-4"),
                            Div(
                                Div(
                                    H3(
                                        "🏗️ Infrastructure & DevOps",
                                        cls="text-lg font-semibold mb-2",
                                    ),
                                    P(
                                        "Kubernetes, Terraform, AWS, GCP—I've built and maintained infrastructure "
                                        "at scale. My expertise includes container orchestration, CI/CD pipelines, "
                                        "and cloud cost optimization.",
                                        cls="text-muted-foreground",
                                    ),
                                    cls="card p-6",
                                ),
                                Div(
                                    H3(
                                        "🔒 Security & Compliance",
                                        cls="text-lg font-semibold mb-2",
                                    ),
                                    P(
                                        "With a focus on healthcare clients, I specialize in HIPAA-compliant "
                                        "architectures and security best practices for sensitive data handling.",
                                        cls="text-muted-foreground",
                                    ),
                                    cls="card p-6",
                                ),
                                Div(
                                    H3(
                                        "📈 Digital Marketing Tech",
                                        cls="text-lg font-semibold mb-2",
                                    ),
                                    P(
                                        "At Seen Web Developers, I build the technical foundation for our "
                                        "marketing services—analytics pipelines, automated reporting, and "
                                        "conversion tracking systems.",
                                        cls="text-muted-foreground",
                                    ),
                                    cls="card p-6",
                                ),
                                cls="grid gap-4 mb-8",
                            ),
                            cls="mb-8",
                        ),
                        # Writing
                        Div(
                            H2(
                                "What I Write About",
                                cls="text-2xl font-bold font-display mb-4",
                            ),
                            Ul(
                                Li(
                                    Strong("Container Orchestration"),
                                    " — Kubernetes patterns, Helm charts, and service mesh",
                                ),
                                Li(
                                    Strong("Infrastructure as Code"),
                                    " — Terraform modules, Pulumi, and GitOps workflows",
                                ),
                                Li(
                                    Strong("Cloud Architecture"),
                                    " — Multi-cloud strategies and cost optimization",
                                ),
                                Li(
                                    Strong("Security & Compliance"),
                                    " — HIPAA, SOC 2, and DevSecOps practices",
                                ),
                                Li(
                                    Strong("Building in Public"),
                                    " — Micro-SaaS journeys and lessons learned",
                                ),
                                cls="space-y-3 text-lg",
                            ),
                            cls="mb-8",
                        ),
                    ),
                    # Sidebar
                    Aside(
                        # Experience card
                        Div(
                            H3("Experience", cls="text-lg font-semibold mb-4"),
                            Div(
                                Div(
                                    Span(
                                        SITE.company_name,
                                        cls="font-semibold text-primary",
                                    ),
                                    Span(
                                        " — CTO & Co-founder",
                                        cls="text-sm text-muted-foreground block",
                                    ),
                                    Span(
                                        "2022 - Present",
                                        cls="text-xs text-muted-foreground",
                                    ),
                                    cls="mb-4 pb-4 border-b border-border",
                                ),
                                Div(
                                    Span("Apple", cls="font-semibold"),
                                    Span(
                                        " — Site Reliability Engineer",
                                        cls="text-sm text-muted-foreground block",
                                    ),
                                    Span(
                                        "2019 - 2022",
                                        cls="text-xs text-muted-foreground",
                                    ),
                                    cls="mb-4 pb-4 border-b border-border",
                                ),
                                Div(
                                    Span("Capital One", cls="font-semibold"),
                                    Span(
                                        " — DevOps Engineer",
                                        cls="text-sm text-muted-foreground block",
                                    ),
                                    Span(
                                        "2017 - 2019",
                                        cls="text-xs text-muted-foreground",
                                    ),
                                ),
                            ),
                            cls="card p-6 mb-6",
                        ),
                        # Skills card
                        Div(
                            H3("Technologies", cls="text-lg font-semibold mb-4"),
                            Div(
                                *[
                                    Span(skill, cls="badge badge-outline")
                                    for skill in [
                                        "Kubernetes",
                                        "Terraform",
                                        "AWS",
                                        "GCP",
                                        "Docker",
                                        "Python",
                                        "Go",
                                        "GitHub Actions",
                                        "ArgoCD",
                                        "Prometheus",
                                        "Grafana",
                                    ]
                                ],
                                cls="flex flex-wrap gap-2",
                            ),
                            cls="card p-6 mb-6",
                        ),
                        # Connect card
                        Div(
                            H3("Connect", cls="text-lg font-semibold mb-4"),
                            A(
                                "GitHub",
                                href=SITE.github_url,
                                target="_blank",
                                cls="block text-muted-foreground hover:text-primary mb-2",
                            ),
                            A(
                                "LinkedIn",
                                href=SITE.linkedin_url,
                                target="_blank",
                                cls="block text-muted-foreground hover:text-primary mb-2",
                            ),
                            A(
                                "Twitter/X",
                                href=f"https://twitter.com/{SITE.twitter_handle.lstrip('@')}",
                                target="_blank",
                                cls="block text-muted-foreground hover:text-primary mb-2",
                            ),
                            A(
                                "Email",
                                href=f"mailto:{SITE.author_email}",
                                cls="block text-muted-foreground hover:text-primary",
                            ),
                            cls="card p-6",
                        ),
                    ),
                    cls="grid md:grid-cols-3 gap-12",
                ),
                cls="max-w-6xl mx-auto px-6",
            ),
            cls="py-16",
        ),
        title="About",
        description=f"Learn about {SITE.author}, a DevOps engineer with 7+ years of experience at Apple and Capital One, now building healthcare technology at {SITE.company_name}.",
        url="/about",
    )


def SponsorshipsPage():
    """Sponsorships page."""
    return Page(
        Section(
            Div(
                SectionHeader(
                    "Sponsorships",
                    "Partner with Ummahrican to reach DevOps professionals.",
                ),
                Div(
                    P(
                        "I work with developer tools, cloud providers, and infrastructure companies "
                        "to create sponsored content that genuinely helps my audience.",
                        cls="text-lg mb-6",
                    ),
                    H2("What I Offer", cls="text-2xl font-bold font-display mb-4"),
                    Div(
                        Div(
                            H3("📝 Sponsored Posts", cls="text-lg font-semibold mb-2"),
                            P(
                                "In-depth tutorials and guides featuring your product. "
                                "Authentic, technical content that provides real value.",
                                cls="text-muted-foreground",
                            ),
                            cls="card p-6",
                        ),
                        Div(
                            H3("🎬 Product Reviews", cls="text-lg font-semibold mb-2"),
                            P(
                                "Honest, hands-on reviews of developer tools and services. "
                                "Real-world testing with transparent feedback.",
                                cls="text-muted-foreground",
                            ),
                            cls="card p-6",
                        ),
                        Div(
                            H3(
                                "📧 Newsletter Sponsorship",
                                cls="text-lg font-semibold mb-2",
                            ),
                            P(
                                "Reach engaged DevOps professionals directly in their inbox. "
                                "Native ad placements in my weekly newsletter.",
                                cls="text-muted-foreground",
                            ),
                            cls="card p-6",
                        ),
                        cls="grid md:grid-cols-3 gap-6 mb-8",
                    ),
                    H2("Past Partners", cls="text-2xl font-bold font-display mb-4"),
                    P(
                        "I've worked with companies focused on cloud infrastructure, "
                        "developer tools, and DevOps practices. Reach out to discuss partnership opportunities.",
                        cls="text-lg text-muted-foreground mb-8",
                    ),
                    A(
                        f"Contact me at {SITE.author_email}",
                        href=f"mailto:{SITE.author_email}?subject=Sponsorship Inquiry",
                        cls="btn btn-primary",
                    ),
                    cls="max-w-4xl",
                ),
                cls="max-w-6xl mx-auto px-6",
            ),
            cls="py-16",
        ),
        title="Sponsorships",
        description="Partner with Ummahrican for sponsored content, product reviews, and newsletter sponsorships reaching DevOps professionals.",
        url="/sponsorships",
    )


def ConsultingPage():
    """Consulting page."""
    return Page(
        Section(
            Div(
                SectionHeader("Consulting", "DevOps expertise for your team."),
                Div(
                    P(
                        "With 7+ years of experience at Apple, Capital One, and now running my own "
                        "infrastructure for healthcare clients, I offer consulting services for teams "
                        "looking to level up their DevOps practices.",
                        cls="text-lg mb-8",
                    ),
                    H2("Services", cls="text-2xl font-bold font-display mb-4"),
                    Div(
                        Div(
                            H3(
                                "Infrastructure Review",
                                cls="text-lg font-semibold mb-2",
                            ),
                            P(
                                "Comprehensive audit of your cloud infrastructure, Kubernetes clusters, "
                                "and CI/CD pipelines with actionable recommendations.",
                                cls="text-muted-foreground",
                            ),
                            cls="card p-6",
                        ),
                        Div(
                            H3("HIPAA Compliance", cls="text-lg font-semibold mb-2"),
                            P(
                                "For healthcare startups: architecture review and implementation guidance "
                                "for HIPAA-compliant infrastructure.",
                                cls="text-muted-foreground",
                            ),
                            cls="card p-6",
                        ),
                        Div(
                            H3("Team Training", cls="text-lg font-semibold mb-2"),
                            P(
                                "Hands-on workshops for your engineering team on Kubernetes, Terraform, "
                                "or DevOps best practices.",
                                cls="text-muted-foreground",
                            ),
                            cls="card p-6",
                        ),
                        cls="grid md:grid-cols-3 gap-6 mb-8",
                    ),
                    A(
                        "Get in Touch",
                        href=f"mailto:{SITE.author_email}?subject=Consulting Inquiry",
                        cls="btn btn-primary",
                    ),
                    cls="max-w-4xl",
                ),
                cls="max-w-6xl mx-auto px-6",
            ),
            cls="py-16",
        ),
        title="Consulting",
        description=f"DevOps consulting services from {SITE.author}. Infrastructure reviews, HIPAA compliance, and team training.",
        url="/consulting",
    )


def register_routes(app, rt):
    """Register static page routes."""

    @rt("/about")
    def get():
        return AboutPage()

    @rt("/sponsorships")
    def get():
        return SponsorshipsPage()

    @rt("/consulting")
    def get():
        return ConsultingPage()
