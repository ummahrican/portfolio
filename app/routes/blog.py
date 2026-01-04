"""
Blog routes: list and detail.
"""

from app.components.layout import ListPage, DetailPage, NotFoundPage
from app.data import get_posts, get_post


def register_routes(app, rt):
    @rt("/blog")
    def get():
        return ListPage(get_posts(), "Blog", "/blog")

    @rt("/blog/{slug}")
    def get(slug: str):
        post = get_post(slug)
        if not post:
            return NotFoundPage("Post Not Found", "This post doesn't exist.", "/blog", "Back to Blog")
        return DetailPage(post, "/blog", "Back to Blog")
