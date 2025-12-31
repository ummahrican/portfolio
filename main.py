from fasthtml.common import *

# Tailwind config for Basecoat integration
tailwind_config = """
tailwind.config = {
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                background: 'oklch(var(--background))',
                foreground: 'oklch(var(--foreground))',
                card: 'oklch(var(--card))',
                'card-foreground': 'oklch(var(--card-foreground))',
                primary: 'oklch(var(--primary))',
                'primary-foreground': 'oklch(var(--primary-foreground))',
                secondary: 'oklch(var(--secondary))',
                'secondary-foreground': 'oklch(var(--secondary-foreground))',
                muted: 'oklch(var(--muted))',
                'muted-foreground': 'oklch(var(--muted-foreground))',
                accent: 'oklch(var(--accent))',
                'accent-foreground': 'oklch(var(--accent-foreground))',
                destructive: 'oklch(var(--destructive))',
                border: 'oklch(var(--border))',
                ring: 'oklch(var(--ring))',
            },
            borderRadius: {
                sm: 'calc(var(--radius) - 4px)',
                md: 'calc(var(--radius) - 2px)',
                lg: 'var(--radius)',
                xl: 'calc(var(--radius) + 4px)',
            }
        }
    }
}
"""

# Custom Mediterranean theme CSS variables + custom styles
custom_css = """
:root {
    /* Mediterranean color palette using oklch */
    --terracotta: 0.55 0.15 35;
    --teal: 0.55 0.12 195;
    --saffron: 0.75 0.15 85;
    --deep-blue: 0.35 0.08 250;
    --olive: 0.50 0.10 120;
    
    /* Override Basecoat defaults with Mediterranean theme */
    --background: 0.98 0.01 90;
    --foreground: 0.25 0.05 250;
    --card: 1 0 0;
    --card-foreground: 0.25 0.05 250;
    --primary: 0.55 0.15 35;
    --primary-foreground: 0.98 0 0;
    --secondary: 0.55 0.12 195;
    --secondary-foreground: 0.98 0 0;
    --muted: 0.95 0.01 90;
    --muted-foreground: 0.50 0.02 250;
    --accent: 0.75 0.15 85;
    --accent-foreground: 0.25 0.05 250;
    --destructive: 0.55 0.2 25;
    --border: 0.90 0.02 90;
    --ring: 0.55 0.15 35;
    --radius: 0.625rem;
}

.dark {
    --background: 0.18 0.04 250;
    --foreground: 0.95 0.01 90;
    --card: 0.22 0.04 250;
    --card-foreground: 0.95 0.01 90;
    --primary: 0.70 0.12 35;
    --primary-foreground: 0.15 0.02 250;
    --secondary: 0.65 0.10 195;
    --secondary-foreground: 0.15 0.02 250;
    --muted: 0.28 0.03 250;
    --muted-foreground: 0.65 0.02 90;
    --accent: 0.70 0.12 85;
    --accent-foreground: 0.18 0.04 250;
    --border: 0.32 0.03 250;
    --ring: 0.70 0.12 35;
}

body {
    font-family: 'Inter', system-ui, sans-serif;
}

/* Hero pattern */
.hero-pattern {
    background: linear-gradient(135deg, oklch(0.35 0.08 250) 0%, oklch(0.45 0.10 195) 100%);
    position: relative;
}

.hero-pattern::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image: 
        radial-gradient(circle at 20% 50%, oklch(0.55 0.15 35 / 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 50%, oklch(0.55 0.12 195 / 0.1) 0%, transparent 50%);
}

/* Decorative divider */
.divider-gradient {
    height: 4px;
    background: linear-gradient(90deg, 
        transparent 0%, 
        oklch(0.55 0.15 35) 20%, 
        oklch(0.75 0.15 85) 50%, 
        oklch(0.55 0.12 195) 80%, 
        transparent 100%
    );
    border-radius: 2px;
}

/* Card hover effect */
.card-hover {
    transition: all 0.3s ease;
}
.card-hover:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px oklch(0.35 0.08 250 / 0.15);
}

/* Custom badge colors */
.badge-terracotta {
    background: oklch(0.55 0.15 35);
    color: white;
}
.badge-teal {
    background: oklch(0.55 0.12 195);
    color: white;
}
.badge-saffron {
    background: oklch(0.75 0.15 85);
    color: oklch(0.25 0.05 250);
}
.badge-olive {
    background: oklch(0.50 0.10 120);
    color: white;
}

/* Playfair Display for headings */
.font-display {
    font-family: 'Playfair Display', serif;
}

/* Footer gradient bar */
.footer-bar {
    height: 4px;
    background: linear-gradient(90deg, 
        oklch(0.55 0.15 35), 
        oklch(0.75 0.15 85), 
        oklch(0.55 0.12 195)
    );
}
"""

# Headers for the app
hdrs = (
    # Tailwind CSS CDN
    Script(src="https://cdn.tailwindcss.com"),
    Script(tailwind_config),
    # BasecoatUI CSS and JS
    Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/basecoat-css@0.3.9/dist/basecoat.cdn.min.css",
    ),
    Script(
        src="https://cdn.jsdelivr.net/npm/basecoat-css@0.3.9/dist/js/all.min.js",
        defer=True,
    ),
    # Google Fonts
    Link(rel="preconnect", href="https://fonts.googleapis.com"),
    Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=True),
    Link(
        rel="stylesheet",
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap",
    ),
    # Lucide icons
    Script(src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"),
    # Custom styles
    Style(custom_css),
)

app, rt = fast_app(hdrs=hdrs, pico=False)

# Sample data
blog_posts = [
    {
        "slug": "kubernetes-zero-to-hero",
        "title": "Kubernetes Zero to Hero: A DevOps Engineer's Journey",
        "excerpt": "From confused kubectl commands to confident cluster management. Here's everything I wish I knew when starting with K8s.",
        "date": "2024-12-28",
        "tags": ["Kubernetes", "DevOps", "Containers"],
        "reading_time": "12 min",
        "featured": True,
    },
    {
        "slug": "terraform-best-practices",
        "title": "Terraform Best Practices I Learned at Capital One",
        "excerpt": "Battle-tested patterns for managing infrastructure at scale. State management, module design, and CI/CD integration.",
        "date": "2024-12-20",
        "tags": ["Terraform", "IaC", "AWS"],
        "reading_time": "8 min",
        "featured": True,
    },
    {
        "slug": "docker-multi-stage-builds",
        "title": "Docker Multi-Stage Builds: Shrink Your Images by 90%",
        "excerpt": "Stop shipping bloated containers. A practical guide to creating minimal, secure Docker images for production.",
        "date": "2024-12-15",
        "tags": ["Docker", "Containers", "Security"],
        "reading_time": "6 min",
        "featured": False,
    },
    {
        "slug": "github-actions-advanced",
        "title": "Advanced GitHub Actions: Beyond Hello World",
        "excerpt": "Custom actions, matrix builds, and secrets management. Level up your CI/CD pipelines.",
        "date": "2024-12-10",
        "tags": ["GitHub Actions", "CI/CD", "Automation"],
        "reading_time": "10 min",
        "featured": False,
    },
]

portfolio_items = [
    {
        "title": "Seen Web Developers",
        "description": "Co-founded a Muslim-owned digital marketing agency specializing in HIPAA-compliant healthcare solutions.",
        "tech": ["Next.js", "Python", "AWS", "HIPAA"],
        "link": "https://seenwebdev.com",
        "type": "Business",
    },
    {
        "title": "Healthcare PACS Integration",
        "description": "Built Picture Archiving and Communication Systems for medical imaging practices.",
        "tech": ["Python", "DICOM", "PostgreSQL", "Docker"],
        "link": "#",
        "type": "Enterprise",
    },
    {
        "title": "SEO Analytics Dashboard",
        "description": "Custom analytics platform for tracking client SEO performance and ROI metrics.",
        "tech": ["React", "FastAPI", "PostgreSQL"],
        "link": "#",
        "type": "Internal Tool",
    },
]

microsaas_projects = [
    {
        "name": "DevOps Checklist",
        "tagline": "Production readiness checklists for startups",
        "status": "live",
        "mrr": "$0 (Free)",
        "users": "150+",
    },
    {
        "name": "InfraSnap",
        "tagline": "Instant infrastructure documentation",
        "status": "beta",
        "mrr": "Coming soon",
        "users": "Beta testers",
    },
    {
        "name": "HealthSEO",
        "tagline": "SEO automation for healthcare practices",
        "status": "building",
        "mrr": "In development",
        "users": "-",
    },
]


# Components
def Tag(text, variant="terracotta"):
    cls_map = {
        "terracotta": "badge badge-terracotta",
        "teal": "badge badge-teal",
        "saffron": "badge badge-saffron",
        "olive": "badge badge-olive",
    }
    return Span(text, cls=cls_map.get(variant, "badge"))


def StatusBadge(status):
    if status == "live":
        return Span("● Live", cls="badge bg-green-500 text-white")
    elif status == "beta":
        return Span("◐ Beta", cls="badge badge-saffron")
    else:
        return Span("◔ Building", cls="badge badge-terracotta")


def Navbar():
    return Header(
        Nav(
            Div(
                A(
                    Span("✦ ", cls="text-[oklch(0.75_0.15_85)]"),
                    Span("Ummahrican", cls="font-bold"),
                    href="/",
                    cls="text-xl text-white flex items-center",
                ),
                cls="flex items-center",
            ),
            Div(
                A(
                    "Blog",
                    href="#blog",
                    cls="text-white/80 hover:text-white px-4 py-2 transition-colors",
                ),
                A(
                    "Portfolio",
                    href="#portfolio",
                    cls="text-white/80 hover:text-white px-4 py-2 transition-colors",
                ),
                A(
                    "Projects",
                    href="#projects",
                    cls="text-white/80 hover:text-white px-4 py-2 transition-colors",
                ),
                A(
                    "About",
                    href="#about",
                    cls="text-white/80 hover:text-white px-4 py-2 transition-colors",
                ),
                cls="flex items-center gap-2",
            ),
            cls="flex justify-between items-center max-w-6xl mx-auto px-6 py-4",
        ),
        cls="bg-[oklch(0.35_0.08_250)] sticky top-0 z-50",
    )


def Hero():
    return Section(
        Div(
            Div(
                Span(
                    "بِسْمِ ٱللَّٰهِ", cls="text-[oklch(0.75_0.15_85)]/80 text-lg mb-4 block"
                ),
                H1(
                    "DevOps Engineer. ",
                    Br(),
                    Span("Entrepreneur. ", cls="text-[oklch(0.75_0.15_85)]"),
                    Br(),
                    "Builder.",
                    cls="text-5xl md:text-6xl font-bold text-white leading-tight mb-6 font-display",
                ),
                P(
                    "7+ years building resilient systems at Apple & Capital One. Now helping healthcare practices grow at ",
                    A(
                        "Seen Web Developers",
                        href="https://seenwebdev.com",
                        cls="text-[oklch(0.75_0.15_85)] underline hover:text-white transition-colors",
                    ),
                    ".",
                    cls="text-xl text-white/80 mb-8 max-w-xl",
                ),
                Div(
                    A("Read the Blog", href="#blog", cls="btn btn-primary"),
                    A(
                        "View Projects",
                        href="#projects",
                        cls="btn btn-outline border-white/30 text-white hover:bg-white/10",
                    ),
                    cls="flex gap-4 flex-wrap",
                ),
                cls="relative z-10 py-20 md:py-32 px-6 max-w-6xl mx-auto",
            ),
        ),
        cls="hero-pattern",
    )


def BlogCard(post, featured=False):
    tag_variants = ["terracotta", "teal", "saffron", "olive"]
    return Article(
        Div(
            Div(
                *[
                    Tag(tag, tag_variants[i % len(tag_variants)])
                    for i, tag in enumerate(post["tags"])
                ],
                cls="flex flex-wrap gap-2 mb-3",
            ),
            H3(
                A(
                    post["title"],
                    href=f"/blog/{post['slug']}",
                    cls="hover:text-primary transition-colors",
                ),
                cls="text-xl font-semibold mb-2 font-display",
            ),
            P(post["excerpt"], cls="text-muted-foreground mb-4"),
            Div(
                Span(post["date"], cls="text-sm text-muted-foreground"),
                Span(" · ", cls="text-muted-foreground"),
                Span(f"📖 {post['reading_time']}", cls="text-sm text-secondary"),
                cls="flex items-center",
            ),
            cls="p-6",
        ),
        cls=f"card card-hover {'border-l-4 border-l-primary' if featured else ''}",
    )


def BlogSection():
    featured = [p for p in blog_posts if p.get("featured")]
    regular = [p for p in blog_posts if not p.get("featured")]

    return Section(
        Div(
            Div(
                Span("✦ ", cls="text-primary"),
                Span("Latest from the Blog", cls="text-3xl font-bold font-display"),
                P(
                    "Technical deep-dives, lessons learned, and DevOps wisdom.",
                    cls="text-muted-foreground mt-2",
                ),
                cls="text-center mb-8",
            ),
            Div(cls="divider-gradient w-24 mx-auto mb-12"),
            Div(
                *[BlogCard(post, featured=True) for post in featured],
                cls="grid md:grid-cols-2 gap-6 mb-8",
            ),
            Div(*[BlogCard(post) for post in regular], cls="grid md:grid-cols-2 gap-6"),
            cls="max-w-6xl mx-auto px-6",
        ),
        id="blog",
        cls="py-20 bg-muted/30",
    )


def PortfolioCard(item):
    tag_variants = ["teal", "terracotta", "saffron", "olive"]
    return Article(
        Div(
            Span(item["type"], cls="badge badge-outline mb-3"),
            H3(item["title"], cls="text-xl font-semibold mb-2 font-display"),
            P(item["description"], cls="text-muted-foreground mb-4"),
            Div(
                *[
                    Tag(tech, tag_variants[i % len(tag_variants)])
                    for i, tech in enumerate(item["tech"])
                ],
                cls="flex flex-wrap gap-2 mb-4",
            ),
            A(
                "View Project →",
                href=item["link"],
                cls="text-primary hover:underline font-medium",
            ),
            cls="p-6",
        ),
        cls="card card-hover",
    )


def PortfolioSection():
    return Section(
        Div(
            Div(
                Span("✦ ", cls="text-secondary"),
                Span("Portfolio", cls="text-3xl font-bold font-display"),
                P(
                    "Selected projects and professional work.",
                    cls="text-muted-foreground mt-2",
                ),
                cls="text-center mb-8",
            ),
            Div(cls="divider-gradient w-24 mx-auto mb-12"),
            Div(
                *[PortfolioCard(item) for item in portfolio_items],
                cls="grid md:grid-cols-3 gap-6",
            ),
            cls="max-w-6xl mx-auto px-6",
        ),
        id="portfolio",
        cls="py-20",
    )


def ProjectCard(project):
    return Article(
        Div(
            StatusBadge(project["status"]),
            H3(project["name"], cls="text-xl font-bold mt-4 mb-1 font-display"),
            P(project["tagline"], cls="text-primary text-sm mb-4"),
            Div(
                Div(
                    Span("MRR", cls="text-xs text-muted-foreground block"),
                    Span(project["mrr"], cls="font-semibold"),
                ),
                Div(
                    Span("Users", cls="text-xs text-muted-foreground block"),
                    Span(project["users"], cls="font-semibold"),
                ),
                cls="grid grid-cols-2 gap-4 pt-4 border-t",
            ),
            cls="p-6",
        ),
        cls="card card-hover border-t-4 border-t-secondary",
    )


def ProjectsSection():
    return Section(
        Div(
            Div(
                Span("✦ ", cls="text-accent"),
                Span("Micro-SaaS Projects", cls="text-3xl font-bold font-display"),
                P(
                    "Building in public. Small tools, big impact.",
                    cls="text-muted-foreground mt-2",
                ),
                cls="text-center mb-8",
            ),
            Div(cls="divider-gradient w-24 mx-auto mb-12"),
            Div(
                *[ProjectCard(project) for project in microsaas_projects],
                cls="grid md:grid-cols-3 gap-6",
            ),
            cls="max-w-6xl mx-auto px-6",
        ),
        id="projects",
        cls="py-20 bg-muted/30",
    )


def AboutSection():
    return Section(
        Div(
            Div(
                Div(
                    Span("✦ ", cls="text-primary"),
                    Span("About Me", cls="text-3xl font-bold font-display"),
                    cls="mb-6",
                ),
                P(
                    "I'm a DevOps engineer turned entrepreneur with a passion for building reliable systems. "
                    "After 7+ years at Apple and Capital One, I co-founded ",
                    A(
                        "Seen Web Developers",
                        href="https://seenwebdev.com",
                        cls="text-primary hover:underline",
                    ),
                    " — a Muslim-owned digital marketing agency specializing in healthcare.",
                    cls="text-lg mb-4",
                ),
                P(
                    "We operate with Islamic business principles, including donating 10% of profits to charity.",
                    cls="text-lg text-muted-foreground mb-6",
                ),
                H4("What I Write About", cls="text-xl font-semibold mb-3"),
                Ul(
                    Li("🐳 Container orchestration & Kubernetes"),
                    Li("🏗️ Infrastructure as Code (Terraform, Pulumi)"),
                    Li("🔒 Security & HIPAA compliance"),
                    Li("💰 Cloud cost optimization"),
                    Li("🚀 CI/CD pipelines & DevOps culture"),
                    cls="space-y-2 text-muted-foreground",
                ),
                cls="md:col-span-2",
            ),
            Div(
                Div(
                    H4("Experience", cls="font-semibold mb-4"),
                    Div(
                        Div(
                            Span("Apple", cls="font-medium"),
                            Span(" — SRE", cls="text-muted-foreground text-sm"),
                            cls="mb-2",
                        ),
                        Div(
                            Span("Capital One", cls="font-medium"),
                            Span(" — DevOps", cls="text-muted-foreground text-sm"),
                            cls="mb-2",
                        ),
                        Div(
                            Span("Seen Web Dev", cls="font-medium text-primary"),
                            Span(" — CTO", cls="text-muted-foreground text-sm"),
                        ),
                    ),
                    cls="card p-6 mb-6",
                ),
                Div(
                    H4("Connect", cls="font-semibold mb-4"),
                    A(
                        "GitHub",
                        href="#",
                        cls="block text-muted-foreground hover:text-primary mb-2",
                    ),
                    A(
                        "LinkedIn",
                        href="#",
                        cls="block text-muted-foreground hover:text-primary mb-2",
                    ),
                    A(
                        "Twitter/X",
                        href="#",
                        cls="block text-muted-foreground hover:text-primary",
                    ),
                    cls="card p-6",
                ),
            ),
            cls="grid md:grid-cols-3 gap-12 max-w-6xl mx-auto px-6",
        ),
        id="about",
        cls="py-20",
    )


def Newsletter():
    return Section(
        Div(
            H2("Stay Updated", cls="text-2xl font-bold text-white mb-2 font-display"),
            P(
                "Get DevOps insights delivered to your inbox. No spam.",
                cls="text-white/80 mb-6",
            ),
            Form(
                Div(
                    Input(
                        type="email",
                        placeholder="your@email.com",
                        cls="input bg-white/10 border-white/20 text-white placeholder:text-white/50",
                    ),
                    Button("Subscribe", type="submit", cls="btn btn-primary"),
                    cls="flex gap-3 flex-wrap justify-center",
                ),
            ),
            cls="text-center py-16 px-6 max-w-xl mx-auto",
        ),
        cls="bg-[oklch(0.35_0.08_250)]",
    )


def SiteFooter():
    return Footer(
        Div(cls="footer-bar"),
        Div(
            Div(
                Div(
                    A(
                        Span("✦ ", cls="text-accent"),
                        Span("Ummahrican", cls="font-bold"),
                        href="/",
                        cls="text-xl text-white mb-4 block",
                    ),
                    P("DevOps Engineer & Entrepreneur", cls="text-white/60 text-sm"),
                ),
                Div(
                    H4("Navigation", cls="text-white font-semibold mb-4"),
                    A(
                        "Blog",
                        href="#blog",
                        cls="text-white/60 hover:text-white block mb-2 text-sm",
                    ),
                    A(
                        "Portfolio",
                        href="#portfolio",
                        cls="text-white/60 hover:text-white block mb-2 text-sm",
                    ),
                    A(
                        "Projects",
                        href="#projects",
                        cls="text-white/60 hover:text-white block mb-2 text-sm",
                    ),
                    A(
                        "About",
                        href="#about",
                        cls="text-white/60 hover:text-white block text-sm",
                    ),
                ),
                Div(
                    H4("Work With Me", cls="text-white font-semibold mb-4"),
                    A(
                        "Sponsorships",
                        href="#",
                        cls="text-white/60 hover:text-white block mb-2 text-sm",
                    ),
                    A(
                        "Consulting",
                        href="#",
                        cls="text-white/60 hover:text-white block mb-2 text-sm",
                    ),
                    A(
                        "Seen Web Dev",
                        href="https://seenwebdev.com",
                        cls="text-white/60 hover:text-white block text-sm",
                    ),
                ),
                cls="grid md:grid-cols-3 gap-8 py-12 px-6 max-w-6xl mx-auto",
            ),
            Div(
                P(
                    "© 2024 Ahmed. Built with ",
                    A(
                        "FastHTML",
                        href="https://fasthtml.dev",
                        cls="text-accent hover:underline",
                    ),
                    " & ",
                    A(
                        "BasecoatUI",
                        href="https://basecoatui.com",
                        cls="text-accent hover:underline",
                    ),
                    ".",
                    cls="text-white/40 text-sm",
                ),
                cls="border-t border-white/10 py-6 px-6 text-center",
            ),
        ),
        cls="bg-[oklch(0.18_0.04_250)]",
    )


# Routes
@rt("/")
def get():
    return (
        Title("Ummahrican | DevOps Engineer & Entrepreneur"),
        Body(
            Navbar(),
            Main(
                Hero(),
                BlogSection(),
                PortfolioSection(),
                ProjectsSection(),
                AboutSection(),
                Newsletter(),
            ),
            SiteFooter(),
            # Initialize Lucide icons
            Script("lucide.createIcons();"),
            cls="bg-background text-foreground min-h-screen",
        ),
    )


@rt("/blog/{slug}")
def get(slug: str):
    post = next((p for p in blog_posts if p["slug"] == slug), None)
    if not post:
        return Title("Not Found"), Main(
            Div(
                H1("Post Not Found", cls="text-3xl font-bold font-display"),
                P("The blog post you're looking for doesn't exist."),
                A("← Back to Home", href="/", cls="btn btn-primary mt-4"),
                cls="text-center py-20 px-6",
            ),
            cls="min-h-screen flex items-center justify-center",
        )

    tag_variants = ["terracotta", "teal", "saffron", "olive"]
    return (
        Title(f"{post['title']} | Ummahrican"),
        Body(
            Navbar(),
            Main(
                Article(
                    Div(
                        Div(
                            *[
                                Tag(tag, tag_variants[i % len(tag_variants)])
                                for i, tag in enumerate(post["tags"])
                            ],
                            cls="flex flex-wrap gap-2 mb-4",
                        ),
                        H1(post["title"], cls="text-4xl font-bold mb-4 font-display"),
                        Div(
                            Span(post["date"], cls="text-muted-foreground"),
                            Span(" · ", cls="text-muted-foreground"),
                            Span(f"📖 {post['reading_time']}", cls="text-secondary"),
                            cls="mb-8",
                        ),
                        Div(cls="divider-gradient w-24 mb-8"),
                        Div(
                            P(
                                "This is a placeholder for the full blog post content. In production, you'd fetch markdown content and render it here.",
                                cls="text-lg mb-6",
                            ),
                            Pre(
                                Code("""# Example Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: awesome-app
spec:
  replicas: 3"""),
                                cls="bg-[oklch(0.18_0.04_250)] text-white p-4 rounded-lg overflow-x-auto mb-6",
                            ),
                            P("Stay tuned for more content!", cls="text-lg"),
                            cls="prose max-w-none",
                        ),
                        A("← Back to Blog", href="/#blog", cls="btn btn-primary mt-8"),
                        cls="max-w-3xl mx-auto py-16 px-6",
                    ),
                )
            ),
            SiteFooter(),
            Script("lucide.createIcons();"),
            cls="bg-background text-foreground min-h-screen",
        ),
    )


serve()
