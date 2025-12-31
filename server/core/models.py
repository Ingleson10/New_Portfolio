from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils import timezone

# -----------------------------
# Constantes de seções (módulo)
# -----------------------------
SECTION_HERO = "hero"
SECTION_SKILLS = "skills"
SECTION_EXPERIENCE = "experience"
SECTION_CERTIFICATIONS = "certifications"
SECTION_EDUCATION = "education"
SECTION_SERVICES = "services"
SECTION_PROJECTS = "projects"
SECTION_LANGUAGES = "languages"
SECTION_CONTACT = "contact"

SECTION_CHOICES = [
    (SECTION_HERO, "Hero"),
    (SECTION_SKILLS, "Skills"),
    (SECTION_EXPERIENCE, "Experience"),
    (SECTION_CERTIFICATIONS, "Certifications"),
    (SECTION_EDUCATION, "Education"),
    (SECTION_SERVICES, "Services"),
    (SECTION_PROJECTS, "Projects"),
    (SECTION_LANGUAGES, "Languages"),
    (SECTION_CONTACT, "Contact"),
]

class UserProfile(models.Model):
    """
    Representa o dono do portfólio.

    Mapeia a tabela existente 'app_user' no PostgreSQL.
    """
    id = models.AutoField(primary_key=True)
    full_name = models.CharField("Nome completo", max_length=150)
    job_title = models.CharField("Cargo / Título profissional", max_length=150)
    short_bio = models.TextField("Biografia curta")
    location = models.CharField("Localização", max_length=100, blank=True, null=True)
    email = models.EmailField("E-mail", unique=True)
    phone = models.CharField("Telefone", max_length=20, blank=True, null=True)
    github_url = models.URLField("GitHub", max_length=255, blank=True, null=True)
    linkedin_url = models.URLField("LinkedIn", max_length=255, blank=True, null=True)
    portfolio_slug = models.SlugField(
        "Slug do portfólio",
        max_length=50,
        unique=True,
        help_text="Identificador único usado na URL pública do portfólio.",
    )
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        db_table = "app_user"
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"
        ordering = ["full_name"]

    def __str__(self) -> str:
        return self.full_name

    def clean(self):
        if not self.portfolio_slug and self.full_name:
            self.portfolio_slug = slugify(self.full_name)


class Skill(models.Model):
    """
    Habilidades técnicas (linguagens, frameworks, ferramentas).
    Mapeia a tabela 'skill'.
    """
    BACKEND = "backend"
    FRONTEND = "frontend"
    DEVOPS = "devops"
    DATABASE = "database"
    OTHER = "other"

    CATEGORY_CHOICES = [
        (BACKEND, "Backend"),
        (FRONTEND, "Frontend"),
        (DEVOPS, "DevOps"),
        (DATABASE, "Banco de dados"),
        (OTHER, "Outros"),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField("Nome", max_length=100)
    category = models.CharField(
        "Categoria",
        max_length=50,
        choices=CATEGORY_CHOICES,
        default=OTHER,
    )
    level = models.CharField("Nível", max_length=50, blank=True, null=True)
    icon_key = models.CharField(
        "Ícone",
        max_length=100,
        blank=True,
        null=True,
        help_text="Chave usada no front para resolver o ícone (ex.: 'python').",
    )
    order_index = models.IntegerField("Ordem", default=0)

    class Meta:
        db_table = "skill"
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        ordering = ["order_index", "name"]
        unique_together = ("name", "category")

    def __str__(self) -> str:
        return self.name


class Experience(models.Model):
    """
    Experiências profissionais exibidas no portfólio.
    Tabela 'experience'.
    """
    id = models.AutoField(primary_key=True)
    company_name = models.CharField("Empresa", max_length=150)
    role = models.CharField("Cargo", max_length=150)
    location = models.CharField("Localização", max_length=100, blank=True, null=True)
    start_date = models.DateField("Data de início")
    end_date = models.DateField("Data de término", blank=True, null=True)
    is_current = models.BooleanField("Emprego atual?", default=False)
    description = models.TextField("Descrição", blank=True, null=True)
    order_index = models.IntegerField("Ordem", default=0)

    class Meta:
        db_table = "experience"
        verbose_name = "Experiência"
        verbose_name_plural = "Experiências"
        ordering = ["order_index", "-start_date"]

    def __str__(self) -> str:
        return f"{self.role} em {self.company_name}"

    def clean(self):
        if self.is_current and self.end_date is not None:
            raise ValidationError(
                {"end_date": "Experiências atuais não devem ter data de término."}
            )
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError(
                {"end_date": "Data de término não pode ser anterior à data de início."}
            )


class Certification(models.Model):
    """
    Certificações / cursos relevantes.
    Tabela 'certification'.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField("Nome da certificação", max_length=200)
    institution = models.CharField("Instituição", max_length=150)
    issue_date = models.DateField("Data de emissão")
    expiration_date = models.DateField(
        "Data de expiração", blank=True, null=True
    )
    credential_id = models.CharField(
        "ID da credencial", max_length=100, blank=True, null=True
    )
    credential_url = models.URLField(
        "URL da credencial", max_length=255, blank=True, null=True
    )
    order_index = models.IntegerField("Ordem", default=0)

    class Meta:
        db_table = "certification"
        verbose_name = "Certificação"
        verbose_name_plural = "Certificações"
        ordering = ["order_index", "-issue_date"]

    def __str__(self) -> str:
        return f"{self.name} - {self.institution}"

    def clean(self):
        if self.expiration_date and self.expiration_date < self.issue_date:
            raise ValidationError(
                {"expiration_date": "Expiração não pode ser antes da emissão."}
            )


class Project(models.Model):
    """
    Projetos a serem exibidos no portfólio.
    Tabela 'project'.
    (Sem relação ManyToMany explícita com Skill, conforme combinado.)
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField("Título", max_length=150)
    slug = models.SlugField(
        "Slug",
        max_length=150,
        unique=True,
        help_text="Usado na URL de detalhes do projeto.",
    )
    short_description = models.TextField("Descrição curta")
    long_description = models.TextField("Descrição completa", blank=True, null=True)
    repo_url = models.URLField("Repositório", max_length=255, blank=True, null=True)
    demo_url = models.URLField("Demo / Deploy", max_length=255, blank=True, null=True)
    highlight = models.BooleanField("Destaque na home?", default=False)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        db_table = "project"
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title

    def clean(self):
        if not self.slug and self.title:
            self.slug = slugify(self.title)


class ContactMessage(models.Model):
    """
    Mensagens enviadas pelo formulário de contato.
    Tabela 'contact_message'.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField("Nome", max_length=150)
    email = models.EmailField("E-mail")
    subject = models.CharField("Assunto", max_length=150)
    message = models.TextField("Mensagem")
    created_at = models.DateTimeField("Recebida em", auto_now_add=True)
    is_read = models.BooleanField("Lida?", default=False)

    class Meta:
        db_table = "contact_message"
        verbose_name = "Mensagem de contato"
        verbose_name_plural = "Mensagens de contato"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.subject} ({self.email})"


class Education(models.Model):
    """
    Formações acadêmicas.
    Tabela 'education'.
    """
    id = models.AutoField(primary_key=True)
    institution = models.CharField("Instituição", max_length=150)
    degree = models.CharField("Curso / Grau", max_length=150)
    field_of_study = models.CharField(
        "Área de estudo", max_length=150, blank=True, null=True
    )
    start_date = models.DateField("Início")
    end_date = models.DateField("Conclusão", blank=True, null=True)
    is_current = models.BooleanField("Cursando atualmente?", default=False)
    description = models.TextField("Descrição", blank=True, null=True)
    order_index = models.IntegerField("Ordem", default=0)

    class Meta:
        db_table = "education"
        verbose_name = "Formação"
        verbose_name_plural = "Formações"
        ordering = ["order_index", "-start_date"]

    def __str__(self) -> str:
        return f"{self.degree} - {self.institution}"

    def clean(self):
        if self.is_current and self.end_date is not None:
            raise ValidationError(
                {"end_date": "Formações atuais não devem ter data de conclusão."}
            )
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError(
                {"end_date": "Conclusão não pode ser antes do início."}
            )


class Service(models.Model):
    """
    Serviços profissionais oferecidos.
    Tabela 'service'.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField("Título do serviço", max_length=150)
    short_description = models.TextField("Descrição curta")
    detailed_description = models.TextField(
        "Descrição detalhada", blank=True, null=True
    )
    icon_key = models.CharField(
        "Ícone", max_length=100, blank=True, null=True
    )
    highlight = models.BooleanField("Destaque?", default=False)
    order_index = models.IntegerField("Ordem", default=0)

    class Meta:
        db_table = "service"
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ["order_index", "title"]

    def __str__(self) -> str:
        return self.title


class Language(models.Model):
    """
    Idiomas falados.
    Tabela 'language'.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField("Idioma", max_length=50)
    level = models.CharField("Nível", max_length=50)
    order_index = models.IntegerField("Ordem", default=0)

    class Meta:
        db_table = "language"
        verbose_name = "Idioma"
        verbose_name_plural = "Idiomas"
        ordering = ["order_index", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.level})"


class SectionConfig(models.Model):
    section_key = models.CharField(
        "Seção",
        max_length=32,
        unique=True,
        choices=SECTION_CHOICES,  # vindo do módulo
    )
    is_enabled = models.BooleanField("Ativa?", default=True)
    order_index = models.IntegerField("Ordem", default=0)

    class Meta:
        db_table = "section_config"
        verbose_name = "Configuração de seção"
        verbose_name_plural = "Configurações de seções"
        ordering = ["order_index"]
        constraints = [
            models.CheckConstraint(
                name="ck_section_key",
                check=models.Q(section_key__in=[c[0] for c in SECTION_CHOICES]),
            ),
        ]

    def __str__(self) -> str:
        return f"{self.section_key} ({'ativa' if self.is_enabled else 'inativa'})"
