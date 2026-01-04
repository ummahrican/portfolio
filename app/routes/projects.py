"""
Projects routes: list and detail.
"""

from app.components.layout import ListPage, DetailPage, NotFoundPage
from app.data import get_projects, get_project


def register_routes(app, rt):
    @rt("/projects")
    def get():
        return ListPage(get_projects(), "Projects", "/projects")

    @rt("/projects/{slug}")
    def get(slug: str):
        project = get_project(slug)
        if not project:
            return NotFoundPage("Project Not Found", "This project doesn't exist.", "/projects", "Back to Projects")
        return DetailPage(project, "/projects", "Back to Projects")
