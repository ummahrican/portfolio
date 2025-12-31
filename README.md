<div align="center">
  <br>
  <h1>Ummahrican</h1>
  <strong>A Mediterranean-inspired DevOps blog built with FastHTML and BasecoatUI</strong>
</div>
<br>
<p align="center">
  <img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/FastHTML-0.12+-teal.svg" alt="FastHTML Version">
  <img src="https://img.shields.io/badge/BasecoatUI-0.3.9-orange.svg" alt="BasecoatUI Version">
  <img src="https://img.shields.io/github/languages/code-size/ummahrican/portfolio" alt="GitHub code size in bytes">
</p>

Ummahrican is a personal blog and portfolio site showcasing DevOps content, technical projects, and micro-SaaS ventures. Built for sponsored content opportunities with platforms like Fly.io and Digital Ocean.

## 💾 Tech Stack

This project uses [FastHTML](https://fasthtml.dev) for the backend and [BasecoatUI](https://basecoatui.com) for styling - a shadcn/ui-style component library that works without React.

## 📖 Prerequisites

In order to run the project we need `python>=3.12` and `uv` for package management.

Install uv following the [official repo](https://docs.astral.sh/uv/getting-started)

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

### Testing with HTTP/2

mkdir -p certs
openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes
uv run python main.py --ssl

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

### TBD

## 🎭 Customization

### Adding Blog Posts

### TBD

### Color Palette

| Color      | Hex       | Usage            |
| ---------- | --------- | ---------------- |
| Terracotta | `#C45B28` | Primary accent   |
| Teal       | `#1B8A8A` | Secondary accent |
| Saffron    | `#E8A838` | Highlights       |
| Deep Blue  | `#1E3A5F` | Headers          |

## 🤝 Contributing

This is a personal blog template. Feel free to fork and customize for your own use!

## 🍕 Community

Questions or feedback? Reach out on [LinkedIn](https://www.linkedin.com/in/anmustafa)

## ⚖️ LICENSE

MIT
