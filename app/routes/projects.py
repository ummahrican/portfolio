"""
Projects/Micro-SaaS routes: listing and individual project pages.
"""

from fasthtml.common import (
    Section,
    Div,
    H1,
    H3,
    P,
    A,
    Span,
    Article,
    Header,
    Aside,
    Footer,
    NotStr,
)

from app.config import SITE
from app.components import (
    ProjectCard,
    SectionHeader,
    Pagination,
    EmptyState,
    StatusBadge,
    TagList,
)
from app.components.layout import Page, ArticlePage
from app.data import get_all_projects, get_project_by_slug


def ProjectsListPage(projects: list, page: int, total_pages: int):
    """Render the projects listing page."""
    # Group by status
    live = [p for p in projects if p.get("status") == "live"]
    beta = [p for p in projects if p.get("status") == "beta"]
    building = [p for p in projects if p.get("status") == "building"]

    return Page(
        Section(
            Div(
                SectionHeader(
                    "Micro-SaaS Projects",
                    "Building in public. Small tools solving real problems.",
                    accent="accent",
                ),
                # Live projects
                Div(
                    H3("🚀 Live", cls="text-xl font-semibold mb-4"),
                    Div(
                        *[ProjectCard(p) for p in live],
                        cls="grid md:grid-cols-3 gap-6",
                    )
                    if live
                    else P("No live projects yet.", cls="text-muted-foreground"),
                    cls="mb-12",
                )
                if live or not (beta or building)
                else None,
                # Beta projects
                Div(
                    H3("🧪 Beta", cls="text-xl font-semibold mb-4"),
                    Div(
                        *[ProjectCard(p) for p in beta],
                        cls="grid md:grid-cols-3 gap-6",
                    ),
                    cls="mb-12",
                )
                if beta
                else None,
                # Building projects
                Div(
                    H3("🔨 Building", cls="text-xl font-semibold mb-4"),
                    Div(
                        *[ProjectCard(p) for p in building],
                        cls="grid md:grid-cols-3 gap-6",
                    ),
                    cls="mb-12",
                )
                if building
                else None,
                # Empty state
                EmptyState(
                    "No projects yet",
                    "Check back soon for new micro-SaaS projects!",
                    "Go Home",
                    "/",
                )
                if not projects
                else None,
                Pagination(page, total_pages, "/projects"),
                cls="max-w-6xl mx-auto px-6",
            ),
            cls="py-16",
        ),
        title="Projects",
        description=f"Explore {SITE.author}'s micro-SaaS projects. Building in public with transparent metrics and progress updates.",
        url="/projects",
    )


def ProjectPage(project: dict):
    """Render an individual project page."""
    breadcrumb = [
        ("Home", "/"),
        ("Projects", "/projects"),
        (project["name"], f"/projects/{project['slug']}"),
    ]

    return ArticlePage(
        Article(
            Header(
                StatusBadge(project.get("status", "building")),
                H1(
                    project["name"],
                    cls="text-4xl md:text-5xl font-bold mt-4 mb-2 font-display",
                ),
                P(project.get("tagline", ""), cls="text-xl text-primary mb-6"),
                Div(cls="divider-gradient w-24 my-8"),
                cls="mb-8",
            ),
            # Metrics
            Aside(
                Div(
                    Div(
                        Span("Status", cls="text-sm text-muted-foreground block mb-1"),
                        StatusBadge(project.get("status", "building")),
                    ),
                    Div(
                        Span("MRR", cls="text-sm text-muted-foreground block mb-1"),
                        Span(project.get("mrr", "N/A"), cls="text-2xl font-bold"),
                    ),
                    Div(
                        Span("Users", cls="text-sm text-muted-foreground block mb-1"),
                        Span(project.get("users", "-"), cls="text-2xl font-bold"),
                    ),
                    Div(
                        Span("Launch", cls="text-sm text-muted-foreground block mb-1"),
                        Span(project.get("launch_date", "TBD"), cls="font-medium"),
                    ),
                    cls="grid grid-cols-2 md:grid-cols-4 gap-6",
                ),
                cls="card p-6 mb-8",
            ),
            # Content
            Div(
                NotStr(project.get("content", "")),
                cls="prose prose-lg max-w-none",
            )
            if project.get("content")
            else Div(
                P(
                    project.get("description", "More details coming soon."),
                    cls="text-lg",
                ),
            ),
            # Tech stack
            Div(
                H3("Tech Stack", cls="text-lg font-semibold mb-4"),
                TagList(project.get("tech", [])),
                cls="my-8",
            )
            if project.get("tech")
            else None,
            # Links
            Div(
                A(
                    "Visit Project →",
                    href=project.get("link", "#"),
                    target="_blank",
                    cls="btn btn-primary",
                )
                if project.get("link") and project.get("link") != "#"
                else None,
                A(
                    "View Source",
                    href=project.get("github", "#"),
                    target="_blank",
                    cls="btn btn-outline",
                )
                if project.get("github")
                else None,
                cls="flex gap-4 flex-wrap my-8",
            )
            if project.get("link") or project.get("github")
            else None,
            # Navigation
            Footer(
                A("← Back to Projects", href="/projects", cls="btn btn-outline"),
                cls="mt-8",
            ),
        ),
        title=project["name"],
        description=project.get("tagline", project.get("description", ""))[:160],
        url=f"/projects/{project['slug']}",
        breadcrumb_items=breadcrumb,
    )


def NotFoundPage():
    """Project not found page."""
    return Page(
        Div(
            H1("Project Not Found", cls="text-4xl font-bold font-display mb-4"),
            P(
                "The project you're looking for doesn't exist.",
                cls="text-muted-foreground mb-6",
            ),
            A("← Back to Projects", href="/projects", cls="btn btn-primary"),
            cls="text-center py-20 px-6 max-w-xl mx-auto",
        ),
        title="Project Not Found",
        description="The requested project could not be found.",
        url="/projects/not-found",
    )


def register_routes(app, rt):
    """Register project routes."""

    @rt("/projects")
    def get(page: int = 1):
        all_projects = get_all_projects()
        per_page = 12
        total_pages = max(1, (len(all_projects) + per_page - 1) // per_page)
        page = max(1, min(page, total_pages))

        start = (page - 1) * per_page
        end = start + per_page
        projects = all_projects[start:end]

        return ProjectsListPage(projects, page, total_pages)

    @rt("/projects/{slug}")
    def get(slug: str):
        project = get_project_by_slug(slug)
        if not project:
            return NotFoundPage()
        return ProjectPage(project)
