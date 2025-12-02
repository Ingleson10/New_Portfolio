from core.models import Project
from django.utils.text import slugify

projects_data = [
    {
        "title": "Sistema de Gerenciamento de Notas com IA",
        "slug": "sistema-gerenciamento-notas-ia",
        "short_description": (
            "Aplicacao de notas com Inteligencia Artificial para "
            "classificar e organizar anotacoes usando Django, React e PostgreSQL."
        ),
        "long_description": (
            "Sistema de gerenciamento de notas que utiliza modelos de NLP "
            "para classificar automaticamente as anotacoes. "
            "Backend em Django, frontend em React e banco PostgreSQL."
        ),
        "repo_url": "https://github.com/Ingleson10/to_do_list",
        "demo_url": None,
        "highlight": True,
    },
    {
        "title": "Django Web Crawler",
        "slug": "django-web-crawler",
        "short_description": (
            "Crawler em Django para explorar sites, coletar dados e "
            "realizar analises como sentimentos e verificacao de links."
        ),
        "long_description": (
            "Sistema automatizado de web crawling desenvolvido em Django. "
            "Extrai dados, navega por paginas, faz analise de sentimentos "
            "e verifica links quebrados."
        ),
        "repo_url": "https://github.com/Ingleson10/Crawler-Django",
        "demo_url": None,
        "highlight": True,
    },
    {
        "title": "Blog API",
        "slug": "blog-api",
        "short_description": (
            "API REST de blog usando Node.js, Express e Sequelize."
        ),
        "long_description": (
            "API completa com CRUD, testes automatizados, estrutura de pastas "
            "organizada e configuracoes de ambiente."
        ),
        "repo_url": "https://github.com/Ingleson10/API-Blog",
        "demo_url": None,
        "highlight": True,
    },
    {
        "title": "API Moveis",
        "slug": "api-moveis",
        "short_description": (
            "API para gerenciamento de moveis usando Node.js, Express e Sequelize."
        ),
        "long_description": (
            "CRUD completo de moveis, filtros, paginacao e autenticacao JWT."
        ),
        "repo_url": "https://github.com/Ingleson10/API-Moveis",
        "demo_url": None,
        "highlight": True,
    },
    {
        "title": "API Finance",
        "slug": "api-finance",
        "short_description": (
            "API financeira com Node.js, TypeScript, GraphQL e Prisma."
        ),
        "long_description": (
            "Projeto seguindo Clean Architecture, DDD e SOLID. "
            "Autenticacao JWT, testes com Jest e pipeline configurado."
        ),
        "repo_url": "https://github.com/Ingleson10/API-Finance",
        "demo_url": None,
        "highlight": True,
    },
]

def run():
    for data in projects_data:
        slug = data["slug"] or slugify(data["title"])

        obj, created = Project.objects.get_or_create(
            slug=slug,
            defaults={
                "title": data["title"],
                "short_description": data["short_description"],
                "long_description": data["long_description"],
                "repo_url": data["repo_url"],
                "demo_url": data["demo_url"],
                "highlight": data["highlight"],
            },
        )

        status = "CRIADO" if created else "JA EXISTE"
        print(f"[{status}] {obj.title} (slug={obj.slug})")
