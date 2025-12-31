"""
Content loading and parsing utilities.
Handles markdown files with YAML frontmatter.
"""

from pathlib import Path
from typing import Optional

import markdown
import yaml

# Content directory (relative to project root)
CONTENT_DIR = Path(__file__).parent.parent.parent / "content"


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """
    Parse YAML frontmatter from markdown content.

    Returns:
        Tuple of (metadata dict, markdown body)
    """
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    try:
        metadata = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        metadata = {}

    body = parts[2].strip()
    return metadata, body


def render_markdown(content: str) -> str:
    """
    Render markdown to HTML with extensions.
    """
    md = markdown.Markdown(
        extensions=[
            "fenced_code",
            "codehilite",
            "tables",
            "toc",
            "meta",
            "smarty",
        ],
        extension_configs={
            "codehilite": {
                "css_class": "highlight",
                "linenums": False,
                "guess_lang": True,
            },
            "toc": {
                "permalink": True,
                "permalink_class": "toc-anchor",
            },
        },
    )
    return md.convert(content)


def calculate_reading_time(content: str) -> str:
    """Calculate estimated reading time."""
    words = len(content.split())
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"


def load_markdown_file(filepath: Path) -> Optional[dict]:
    """
    Load and parse a single markdown file.

    Returns dict with metadata and rendered content.
    """
    if not filepath.exists():
        return None

    content = filepath.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(content)

    # Calculate reading time from raw content
    reading_time = calculate_reading_time(body)

    # Render markdown to HTML
    html_content = render_markdown(body)

    # Get slug from filename
    slug = filepath.stem

    return {
        "slug": slug,
        "content": html_content,
        "raw_content": body,
        "reading_time": reading_time,
        **metadata,
    }


def load_content_directory(content_type: str) -> list[dict]:
    """
    Load all markdown files from a content directory.

    Args:
        content_type: 'blog', 'portfolio', or 'projects'

    Returns:
        List of parsed content dicts, sorted by date (newest first)
    """
    content_path = CONTENT_DIR / content_type

    if not content_path.exists():
        return []

    items = []
    for filepath in content_path.glob("*.md"):
        item = load_markdown_file(filepath)
        if item:
            items.append(item)

    # Sort by date (newest first)
    items.sort(key=lambda x: x.get("date", ""), reverse=True)
    return items


def get_post_by_slug(slug: str) -> Optional[dict]:
    """Get a single blog post by slug."""
    filepath = CONTENT_DIR / "blog" / f"{slug}.md"
    return load_markdown_file(filepath)


def get_portfolio_item_by_slug(slug: str) -> Optional[dict]:
    """Get a single portfolio item by slug."""
    filepath = CONTENT_DIR / "portfolio" / f"{slug}.md"
    return load_markdown_file(filepath)


def get_project_by_slug(slug: str) -> Optional[dict]:
    """Get a single project by slug."""
    filepath = CONTENT_DIR / "projects" / f"{slug}.md"
    return load_markdown_file(filepath)


def get_all_posts() -> list[dict]:
    """Get all blog posts."""
    return load_content_directory("blog")


def get_all_portfolio() -> list[dict]:
    """Get all portfolio items."""
    return load_content_directory("portfolio")


def get_all_projects() -> list[dict]:
    """Get all projects."""
    return load_content_directory("projects")


def get_featured_posts(limit: int = 2) -> list[dict]:
    """Get featured blog posts."""
    posts = get_all_posts()
    featured = [p for p in posts if p.get("featured", False)]
    return featured[:limit]


def get_recent_posts(limit: int = 4, exclude_featured: bool = False) -> list[dict]:
    """Get recent blog posts."""
    posts = get_all_posts()
    if exclude_featured:
        posts = [p for p in posts if not p.get("featured", False)]
    return posts[:limit]


def get_posts_by_tag(tag: str) -> list[dict]:
    """Get posts filtered by tag."""
    posts = get_all_posts()
    return [p for p in posts if tag.lower() in [t.lower() for t in p.get("tags", [])]]


def get_all_tags() -> list[tuple[str, int]]:
    """
    Get all tags with counts.

    Returns list of (tag, count) tuples sorted by count descending.
    """
    posts = get_all_posts()
    tag_counts = {}

    for post in posts:
        for tag in post.get("tags", []):
            tag_lower = tag.lower()
            tag_counts[tag_lower] = tag_counts.get(tag_lower, 0) + 1

    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_tags
