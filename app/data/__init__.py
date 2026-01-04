"""
Content loading from Markdown files.
Handles blog, portfolio, and projects with consistent frontmatter.
"""

from pathlib import Path
from typing import Optional
import markdown
import yaml

CONTENT_DIR = Path(__file__).parent.parent.parent / "content"


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        metadata = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        metadata = {}
    return metadata, parts[2].strip()


def render_markdown(content: str) -> str:
    """Render markdown to HTML."""
    md = markdown.Markdown(
        extensions=["fenced_code", "codehilite", "tables", "toc"],
        extension_configs={
            "codehilite": {"css_class": "highlight", "linenums": False},
        },
    )
    return md.convert(content)


def load_item(filepath: Path) -> Optional[dict]:
    """Load a single markdown file."""
    if not filepath.exists():
        return None
    content = filepath.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(content)
    
    # Normalize frontmatter fields
    return {
        "slug": filepath.stem,
        "title": metadata.get("title", metadata.get("name", filepath.stem)),
        "date": str(metadata.get("date", "")),
        "summary": metadata.get("summary", metadata.get("excerpt", metadata.get("description", metadata.get("tagline", "")))),
        "tags": metadata.get("tags", metadata.get("tech", [])),
        "content": render_markdown(body),
        "raw": body,
        **metadata,  # Keep all original fields too
    }


def load_collection(content_type: str) -> list[dict]:
    """Load all items from a content directory, sorted by date desc."""
    path = CONTENT_DIR / content_type
    if not path.exists():
        return []
    items = [load_item(f) for f in path.glob("*.md")]
    items = [i for i in items if i]
    items.sort(key=lambda x: x.get("date", ""), reverse=True)
    return items


def get_item(content_type: str, slug: str) -> Optional[dict]:
    """Get a single item by slug."""
    filepath = CONTENT_DIR / content_type / f"{slug}.md"
    return load_item(filepath)


# Convenience functions
def get_posts() -> list[dict]:
    return load_collection("blog")

def get_portfolio() -> list[dict]:
    return load_collection("portfolio")

def get_projects() -> list[dict]:
    return load_collection("projects")

def get_post(slug: str) -> Optional[dict]:
    return get_item("blog", slug)

def get_portfolio_item(slug: str) -> Optional[dict]:
    return get_item("portfolio", slug)

def get_project(slug: str) -> Optional[dict]:
    return get_item("projects", slug)
