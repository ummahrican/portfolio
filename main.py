#!/usr/bin/env python3
"""
Ummahrican - DevOps Portfolio

Run: uv run python main.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5001"))
    reload = os.getenv("RELOAD", "true").lower() == "true"

    print(f"🌐 Starting server on http://{host}:{port}")
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=reload,
        reload_dirs=["app", "content"] if reload else None,
    )


if __name__ == "__main__":
    main()
