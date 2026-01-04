"""
Portfolio routes: list and detail.
"""

from app.components.layout import ListPage, DetailPage, NotFoundPage
from app.data import get_portfolio, get_portfolio_item


def register_routes(app, rt):
    @rt("/portfolio")
    def get():
        return ListPage(get_portfolio(), "Portfolio", "/portfolio")

    @rt("/portfolio/{slug}")
    def get(slug: str):
        item = get_portfolio_item(slug)
        if not item:
            return NotFoundPage("Project Not Found", "This portfolio item doesn't exist.", "/portfolio", "Back to Portfolio")
        return DetailPage(item, "/portfolio", "Back to Portfolio")
