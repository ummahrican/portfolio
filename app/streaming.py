"""
HTMS-style HTML streaming with robust error handling.

Key principle: Once streaming starts, we cannot change HTTP status.
All errors must be handled within the stream itself.
"""

import asyncio
import uuid
import logging
from typing import Callable, Any, Optional
from dataclasses import dataclass
from starlette.responses import StreamingResponse

logger = logging.getLogger(__name__)

# Configuration
CHUNK_TIMEOUT_SECONDS = 10
MAX_RETRIES = 2


@dataclass
class ChunkConfig:
    """Configuration for a streaming chunk."""

    id: str
    fetcher: Callable
    fallback_html: str = (
        "<span class='text-muted-foreground'>Content unavailable</span>"
    )
    timeout: float = CHUNK_TIMEOUT_SECONDS
    retries: int = MAX_RETRIES
    critical: bool = False  # If True, pre-validate before streaming


@dataclass
class StreamError:
    """Structured error for chunk failures."""

    chunk_id: str
    error_type: str
    message: str
    recoverable: bool = True


def generate_chunk_id(prefix: str = "chunk") -> str:
    """Generate unique chunk ID for this request."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def StreamPlaceholder(
    chunk_id: str,
    fallback: Any = "Loading...",
    error_fallback: Any = None,
    cls: str = "",
):
    """
    Create a placeholder element that will be replaced by streamed content.

    Args:
        chunk_id: Unique identifier for this placeholder
        fallback: Content shown while loading (can be a skeleton component)
        error_fallback: Content shown if streaming fails (optional)
        cls: Additional CSS classes
    """
    from fasthtml.common import Div, NotStr

    # Convert component to string if needed
    if hasattr(fallback, "__ft__") or hasattr(fallback, "__html__"):
        fallback = str(fallback)

    error_html = str(error_fallback) if error_fallback else ""

    return Div(
        NotStr(str(fallback)),
        data_htms_uuid=chunk_id,
        data_htms_error_fallback=error_html,
        cls=f"htms-placeholder {cls}".strip(),
    )


async def fetch_with_timeout(
    fetcher: Callable, timeout: float, retries: int = 0
) -> tuple[Optional[str], Optional[StreamError]]:
    """
    Execute fetcher with timeout and retry logic.

    Returns:
        Tuple of (content, error) - one will be None
    """
    last_error = None

    for attempt in range(retries + 1):
        try:
            # Handle both async and sync fetchers
            if asyncio.iscoroutinefunction(fetcher):
                result = await asyncio.wait_for(fetcher(), timeout=timeout)
            else:
                result = await asyncio.wait_for(
                    asyncio.to_thread(fetcher), timeout=timeout
                )
            return (result, None)

        except asyncio.TimeoutError:
            last_error = StreamError(
                chunk_id="",
                error_type="timeout",
                message=f"Request timed out after {timeout}s",
                recoverable=True,
            )
            logger.warning(f"Chunk timeout (attempt {attempt + 1}/{retries + 1})")

        except Exception as e:
            last_error = StreamError(
                chunk_id="",
                error_type=type(e).__name__,
                message=str(e),
                recoverable=False,
            )
            logger.error(f"Chunk error (attempt {attempt + 1}/{retries + 1}): {e}")

        # Brief delay before retry
        if attempt < retries:
            await asyncio.sleep(0.5 * (attempt + 1))

    return (None, last_error)


def render_error_chunk(chunk_id: str, error: StreamError, fallback_html: str) -> str:
    """
    Render an error state for a failed chunk.

    The error chunk includes:
    - Fallback content for display
    - Data attributes for client-side error handling
    - Optional retry button
    """
    retry_button = ""
    if error.recoverable:
        retry_button = f"""
            <button 
                class="text-sm text-blue-600 hover:underline mt-2"
                onclick="window.htmsRetry && window.htmsRetry('{chunk_id}')"
            >
                Try again
            </button>
        """

    return f'''<htms-chunk 
        uuid="{chunk_id}" 
        data-error="true"
        data-error-type="{error.error_type}"
        data-recoverable="{str(error.recoverable).lower()}"
    >
        <div class="htms-error" role="alert">
            {fallback_html}
            {retry_button}
        </div>
    </htms-chunk>
'''


def render_success_chunk(chunk_id: str, content: str) -> str:
    """Render a successful chunk."""
    return f'<htms-chunk uuid="{chunk_id}">{content}</htms-chunk>\n'


async def stream_html(
    initial_html: str, chunks: dict[str, ChunkConfig], close_html: str = ""
):
    """
    Async generator that streams HTML with HTMS chunks.

    Args:
        initial_html: Initial HTML skeleton (should NOT close </body></html>)
        chunks: Dict mapping chunk_id to ChunkConfig
        close_html: HTML to append after all chunks (typically </body></html>)

    Yields:
        HTML strings progressively
    """
    # Yield initial HTML immediately
    yield initial_html

    # Process chunks concurrently
    async def process_chunk(chunk_id: str, config: ChunkConfig) -> str:
        content, error = await fetch_with_timeout(
            config.fetcher, config.timeout, config.retries
        )

        if error:
            error.chunk_id = chunk_id
            logger.error(
                f"Chunk {chunk_id} failed: {error.error_type} - {error.message}"
            )
            return render_error_chunk(chunk_id, error, config.fallback_html)

        return render_success_chunk(chunk_id, content)

    # Create tasks for all chunks
    tasks = {
        chunk_id: asyncio.create_task(process_chunk(chunk_id, config))
        for chunk_id, config in chunks.items()
    }

    # Yield chunks as they complete (not in order - that's the point!)
    for coro in asyncio.as_completed(tasks.values()):
        try:
            chunk_html = await coro
            yield chunk_html
        except Exception as e:
            # This shouldn't happen due to internal error handling, but just in case
            logger.error(f"Unexpected error in chunk streaming: {e}")
            continue

    # Close the HTML document
    if close_html:
        yield close_html


async def validate_critical_data(chunks: dict[str, ChunkConfig]) -> Optional[str]:
    """
    Pre-validate critical chunks before streaming starts.

    Returns error message if validation fails, None if OK.
    """
    critical_chunks = {
        chunk_id: config for chunk_id, config in chunks.items() if config.critical
    }

    if not critical_chunks:
        return None

    for chunk_id, config in critical_chunks.items():
        try:
            # Quick validation - try to execute the fetcher
            content, error = await fetch_with_timeout(
                config.fetcher,
                timeout=min(config.timeout, 3.0),  # Quick validation
                retries=0,
            )
            if error:
                return f"Critical data unavailable: {chunk_id}"
        except Exception as e:
            return f"Critical data error: {chunk_id}"

    return None


def streaming_page(
    initial_html: str,
    chunks: dict[str, ChunkConfig],
    close_html: str = "</body></html>",
    validate_critical: bool = True,
) -> StreamingResponse:
    """
    Create a StreamingResponse for HTMS-style progressive HTML.

    Args:
        initial_html: Opening HTML (without closing tags)
        chunks: Chunk configurations
        close_html: Closing HTML tags
        validate_critical: Whether to validate critical chunks first

    Returns:
        StreamingResponse with chunked transfer encoding
    """

    async def generate():
        # Optional: Validate critical data before streaming
        if validate_critical:
            error = await validate_critical_data(chunks)
            if error:
                # We haven't started streaming yet, so we can return an error page
                yield f"""
                    <!DOCTYPE html>
                    <html>
                    <head><title>Error</title></head>
                    <body>
                        <h1>Unable to load page</h1>
                        <p>{error}</p>
                        <a href="/">Return home</a>
                    </body>
                    </html>
                """
                return

        # Stream the page
        async for chunk in stream_html(initial_html, chunks, close_html):
            yield chunk

    return StreamingResponse(
        generate(),
        media_type="text/html; charset=utf-8",
        headers={
            "Transfer-Encoding": "chunked",
            "X-Content-Type-Options": "nosniff",
            "Cache-Control": "no-cache",  # Don't cache partial responses
        },
    )


# === Convenience functions for common patterns ===


def simple_chunk(fetcher: Callable, fallback: str = "Loading...") -> ChunkConfig:
    """Create a simple non-critical chunk config."""
    return ChunkConfig(id=generate_chunk_id(), fetcher=fetcher, fallback_html=fallback)


def critical_chunk(fetcher: Callable, fallback: str = "Loading...") -> ChunkConfig:
    """Create a critical chunk that's validated before streaming."""
    return ChunkConfig(
        id=generate_chunk_id(), fetcher=fetcher, fallback_html=fallback, critical=True
    )


def api_chunk(
    fetcher: Callable, fallback: str = "Loading...", timeout: float = 5.0
) -> ChunkConfig:
    """Create a chunk for external API calls with shorter timeout."""
    return ChunkConfig(
        id=generate_chunk_id(),
        fetcher=fetcher,
        fallback_html=fallback,
        timeout=timeout,
        retries=1,  # One retry for API calls
    )
