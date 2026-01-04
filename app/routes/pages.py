"""
Static pages: About, Consulting, Sponsorships.
"""

from fasthtml.common import Section, Div, H1, H2, P, A, Ul, Li
from app.config import SITE
from app.components.layout import Page


def register_routes(app, rt):
    @rt("/about")
    def get():
        return Page(
            Section(
                Div(
                    H1("About", cls="text-3xl font-bold font-display mb-6"),
                    P(
                        f"DevOps engineer with 7+ years at Apple and Capital One. "
                        f"Now CTO at {SITE.company_name}.",
                        cls="text-lg mb-4",
                    ),
                    H2("What I Do", cls="text-2xl font-bold font-display mt-8 mb-4"),
                    Ul(
                        Li("Infrastructure & DevOps (Kubernetes, Terraform, AWS)"),
                        Li("Security & Compliance (HIPAA)"),
                        Li("CI/CD pipelines"),
                        cls="space-y-2 text-muted-foreground",
                    ),
                    cls="max-w-4xl mx-auto px-6",
                ),
                cls="py-16",
            ),
            title="About",
        )

    @rt("/consulting")
    def get():
        return Page(
            Section(
                Div(
                    H1("Consulting", cls="text-3xl font-bold font-display mb-6"),
                    P("DevOps expertise for your team.", cls="text-lg mb-4"),
                    P(
                        "Infrastructure reviews, HIPAA compliance, and team training.",
                        cls="text-muted-foreground mb-6",
                    ),
                    A(f"Contact: {SITE.author_email}", href=f"mailto:{SITE.author_email}", cls="btn btn-primary"),
                    cls="max-w-4xl mx-auto px-6",
                ),
                cls="py-16",
            ),
            title="Consulting",
        )

    @rt("/sponsorships")
    def get():
        return Page(
            Section(
                Div(
                    H1("Sponsorships", cls="text-3xl font-bold font-display mb-6"),
                    P("Partner with Ummahrican to reach DevOps professionals.", cls="text-lg mb-4"),
                    A(f"Contact: {SITE.author_email}", href=f"mailto:{SITE.author_email}", cls="btn btn-primary"),
                    cls="max-w-4xl mx-auto px-6",
                ),
                cls="py-16",
            ),
            title="Sponsorships",
        )
