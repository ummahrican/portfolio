#!/usr/bin/env python3
"""
Ummahrican - Mediterranean-inspired DevOps Blog

Entry point for the application. Run with:
    uv run python main.py

For production with HTTP/2 (requires SSL):
    uv run python main.py --ssl

Environment variables:
    PORT: Server port (default: 5001)
    HOST: Server host (default: 0.0.0.0)
    RELOAD: Enable auto-reload (default: true in dev)
"""

import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """Run the application."""
    import uvicorn

    # Server configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5001"))
    reload = os.getenv("RELOAD", "true").lower() == "true"

    # Check for SSL/HTTP2 mode
    ssl_mode = (
        "--ssl" in sys.argv or os.getenv("SSL_ENABLED", "false").lower() == "true"
    )

    # Uvicorn configuration
    config = {
        "host": host,
        "port": port,
        "reload": reload and not ssl_mode,  # Disable reload in SSL mode
        "reload_dirs": ["app", "content"] if (reload and not ssl_mode) else None,
        "log_level": "info",
    }

    # HTTP/2 requires SSL certificates
    # For production on Fly.io, the edge handles HTTP/2 termination
    # For local development with HTTP/2:
    if ssl_mode:
        ssl_keyfile = os.getenv("SSL_KEYFILE", "certs/key.pem")
        ssl_certfile = os.getenv("SSL_CERTFILE", "certs/cert.pem")

        if os.path.exists(ssl_keyfile) and os.path.exists(ssl_certfile):
            config.update(
                {
                    "ssl_keyfile": ssl_keyfile,
                    "ssl_certfile": ssl_certfile,
                    "http": "h2",  # Enable HTTP/2
                }
            )
            print(f"🔒 Starting with HTTP/2 + SSL on https://{host}:{port}")
        else:
            print("⚠️  SSL certificates not found. Generate with:")
            print("   mkdir -p certs")
            print(
                "   openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes"
            )
            print(f"\n🌐 Starting without SSL on http://{host}:{port}")
    else:
        print(f"🌐 Starting server on http://{host}:{port}")

    # Use string import for reload to work properly
    uvicorn.run("app:app", **config)


if __name__ == "__main__":
    main()
