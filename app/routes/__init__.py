"""
Routes package - register all routes.
"""

from app.routes import home, blog, portfolio, projects, pages, api


def register_all_routes(app, rt):
    home.register_routes(app, rt)
    blog.register_routes(app, rt)
    portfolio.register_routes(app, rt)
    projects.register_routes(app, rt)
    pages.register_routes(app, rt)
    api.register_routes(app, rt)
