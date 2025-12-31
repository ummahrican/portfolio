<div align="center">
  <br>
  <h1>Ummahrican</h1>
  <strong>A Mediterranean-inspired DevOps blog built with FastHTML and BasecoatUI</strong>
</div>
<br>
<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/FastHTML-0.12+-teal.svg" alt="FastHTML Version">
  <img src="https://img.shields.io/badge/BasecoatUI-0.3.9-orange.svg" alt="BasecoatUI Version">
  <img src="https://img.shields.io/github/languages/code-size/ummahrican/portfolio" alt="GitHub code size in bytes">
</p>

Ummahrican is a personal blog and portfolio site showcasing DevOps content, technical projects, and micro-SaaS ventures. Built for sponsored content opportunities with platforms like Fly.io and Digital Ocean.

## 📖 Prerequisites

In order to run the project we need `python>=3.11` and `uv` for package management.

Install uv following the [official repo](https://github.com/astral-sh/uv?tab=readme-ov-file#getting-started)

## 🖥️ Local development

To install the application:

```shell
uv sync --frozen --no-cache
```

To start a local copy of the app on port `5001`:

```shell
uv run python main.py
```

To upgrade packages to latest version for maintenance:

```shell
uv sync --upgrade
```

## 📦 Docker builds

Simply build the dockerfile in your preferred architecture with (select arch with --platform= otherwise it defaults to your system):

```shell
docker build -t ummahrican-blog .
```

Then run it!

```shell
docker run -d -p 5001:5001 ummahrican-blog
```

## 🎨 Code linting

To check the code and styles quality, use the following command:

```shell
# Lint your code
uvx ruff check

# Format your code
uvx ruff format
```

## 🚀 Production deployment

Deploy to Fly.io:

```shell
fly auth login
fly launch
fly deploy
```

Or use the included `fly.toml` configuration.

## 🎭 Customization

### Adding Blog Posts

Edit the `blog_posts` list in `main.py`:

```python
blog_posts = [
    {
        "slug": "your-post-slug",
        "title": "Your Post Title",
        "excerpt": "Brief description...",
        "date": "2024-12-30",
        "tags": ["Kubernetes", "DevOps"],
        "reading_time": "5 min",
        "featured": True
    },
]
```

### Color Palette

| Color      | Hex       | Usage            |
| ---------- | --------- | ---------------- |
| Terracotta | `#C45B28` | Primary accent   |
| Teal       | `#1B8A8A` | Secondary accent |
| Saffron    | `#E8A838` | Highlights       |
| Deep Blue  | `#1E3A5F` | Headers          |

## 💾 Tech Stack

This project uses [FastHTML](https://fasthtml.dev) for the backend and [BasecoatUI](https://basecoatui.com) for styling - a shadcn/ui-style component library that works without React.

## 🤝 Contributing

This is a personal blog template. Feel free to fork and customize for your own use!

## 🍕 Community

Questions or feedback? Reach out on [Twitter/X](https://twitter.com/yourusername) or [LinkedIn](https://linkedin.com/in/yourusername).

## ⚖️ LICENSE

MIT © [ahmed.dev](LICENSE)
