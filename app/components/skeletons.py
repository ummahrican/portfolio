"""
Loading skeleton components for HTMS streaming.
These provide visual placeholders while content loads.
"""

from fasthtml.common import Div, Span, I, P, A


def SkeletonBox(height: str = "h-4", width: str = "w-full", cls: str = ""):
    """Basic skeleton rectangle."""
    return Div(cls=f"htms-skeleton {height} {width} {cls}")


def SkeletonText(lines: int = 3, cls: str = ""):
    """Skeleton text block with multiple lines."""
    return Div(
        *[
            SkeletonBox(
                height="h-4", width="w-full" if i < lines - 1 else "w-2/3", cls="mb-2"
            )
            for i in range(lines)
        ],
        cls=cls,
    )


def FeaturedCardSkeleton():
    """Skeleton for a featured blog post card."""
    return Div(
        SkeletonBox(height="h-48", cls="rounded-lg mb-4"),
        SkeletonBox(height="h-4", width="w-1/4", cls="mb-2"),
        SkeletonBox(height="h-6", width="w-3/4", cls="mb-2"),
        SkeletonText(lines=2),
        cls="card p-4",
    )


def FeaturedSkeleton(count: int = 2):
    """Skeleton for featured posts section."""
    return Div(
        *[FeaturedCardSkeleton() for _ in range(count)], cls="grid md:grid-cols-2 gap-6"
    )


def PostCardSkeleton():
    """Skeleton for a compact blog post card."""
    return Div(
        SkeletonBox(height="h-4", width="w-1/4", cls="mb-2"),
        SkeletonBox(height="h-5", width="w-full", cls="mb-2"),
        SkeletonText(lines=2),
        SkeletonBox(height="h-4", width="w-1/3", cls="mt-2"),
        cls="card p-4",
    )


def PostGridSkeleton(count: int = 4):
    """Skeleton for post grid."""
    return Div(
        *[PostCardSkeleton() for _ in range(count)], cls="grid md:grid-cols-2 gap-6"
    )


def StatCardSkeleton():
    """Skeleton for a stat card (GitHub stars, MRR, etc.)."""
    return Div(
        SkeletonBox(height="h-8", width="w-16", cls="mb-2"),
        SkeletonBox(height="h-4", width="w-24"),
        cls="flex flex-col items-center p-4",
    )


def StatsSkeleton(count: int = 3):
    """Skeleton for stats row."""
    return Div(
        *[StatCardSkeleton() for _ in range(count)], cls="flex gap-6 justify-center"
    )


def ProjectCardSkeleton():
    """Skeleton for project card."""
    return Div(
        Div(SkeletonBox(height="h-6", width="w-16", cls="rounded-full"), cls="mb-3"),
        SkeletonBox(height="h-6", width="w-2/3", cls="mb-2"),
        SkeletonBox(height="h-4", width="w-full", cls="mb-1"),
        SkeletonBox(height="h-4", width="w-3/4", cls="mb-4"),
        Div(
            SkeletonBox(height="h-6", width="w-20"),
            SkeletonBox(height="h-6", width="w-20"),
            cls="flex gap-2",
        ),
        cls="card p-6",
    )


def ErrorFallback(message: str = "Unable to load content"):
    """Generic error fallback component."""
    return Div(
        Div(
            I(data_lucide="alert-circle", cls="w-5 h-5 text-destructive"),
            Span(message, cls="text-muted-foreground"),
            cls="flex items-center gap-2 justify-center",
        ),
        cls="p-4 text-center",
    )


def RetryableFallback(message: str = "Unable to load content"):
    """Error fallback with retry hint."""
    return Div(
        Div(
            I(data_lucide="alert-circle", cls="w-5 h-5 text-amber-500"),
            Span(message, cls="text-muted-foreground"),
            cls="flex items-center gap-2 justify-center",
        ),
        P(
            "This content will retry automatically or ",
            A(
                "refresh the page",
                href="javascript:location.reload()",
                cls="text-primary hover:underline",
            ),
            ".",
            cls="text-sm text-muted-foreground mt-2 text-center",
        ),
        cls="p-4",
    )
