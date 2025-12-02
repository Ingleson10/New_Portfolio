import json

from django.http import JsonResponse, Http404
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt   # 👈 novo
from django.core.mail import send_mail                 # 👈 novo
from django.conf import settings                       # 👈 novo
from django.core.mail import EmailMultiAlternatives  # novo
from django.conf import settings

from .models import (
    UserProfile,
    Skill,
    Experience,
    Certification,
    Project,
    ContactMessage,
    Education,
    Service,
    Language,
    SectionConfig,
)

from .serializers import (
    user_profile_to_dict,
    skill_to_dict,
    experience_to_dict,
    certification_to_dict,
    project_to_dict,
    education_to_dict,
    service_to_dict,
    language_to_dict,
    section_config_to_dict,
    contact_message_to_dict,
)

# ---------- Helpers gerais ----------

def api_error(message: str, status: int = 400, extra: dict | None = None):
    """
    Helper para respostas de erro padronizadas.
    """
    payload = {"error": message}
    if extra:
        payload.update(extra)
    return JsonResponse(payload, status=status)


# ---------- ENDPOINT DE CONTATO (COM CSRF EXEMPT) ----------

@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(require_http_methods(["POST"]), name="dispatch")
class ContactCreateView(View):
    """
    Endpoint para criação de mensagem de contato.

    - Espera JSON no body.
    - Faz validação básica e salva em contact_message.
    - Envia e-mail automático (texto + HTML) para o dono do portfólio.
    """

    def post(self, request, *args, **kwargs):
        try:
            body_unicode = request.body.decode("utf-8")
            try:
                payload = json.loads(body_unicode)
            except json.JSONDecodeError:
                return api_error("JSON inválido.", status=400)

            name = payload.get("name", "").strip()
            email = payload.get("email", "").strip()
            subject = payload.get("subject", "").strip()
            message = payload.get("message", "").strip()

            if not name or not email or not subject or not message:
                return api_error(
                    "Campos obrigatórios: name, email, subject, message.",
                    status=400,
                )

            contact = ContactMessage(
                name=name,
                email=email,
                subject=subject,
                message=message,
            )

            try:
                contact.full_clean()
            except ValidationError as exc:
                return api_error(
                    "Erro de validação.",
                    status=400,
                    extra={"fields": exc.message_dict},
                )

            contact.save()

            # --------- E-MAIL: TEXTO + HTML BONITÃO ---------

            owner_email = settings.DEFAULT_FROM_EMAIL
            logo_url = getattr(settings, "PORTFOLIO_LOGO_URL", None)

            email_subject = f"[Portfólio] Nova mensagem de {name}: {subject}"

            # Texto puro (fallback)
            text_content = (
                "Você recebeu uma nova mensagem pelo portfólio.\n\n"
                f"Nome: {name}\n"
                f"E-mail: {email}\n"
                f"Assunto: {subject}\n\n"
                "Mensagem:\n"
                f"{message}\n"
            )

            # HTML estiloso
            html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <title>Nova mensagem de contato</title>
  </head>
  <body style="margin:0;padding:0;background-color:#0b1120;font-family:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="padding:24px 0;">
      <tr>
        <td align="center">
          <table width="600" cellpadding="0" cellspacing="0" style="background-color:#020617;border-radius:16px;border:1px solid #1f2937;overflow:hidden;">
            <tr>
              <td style="padding:16px 24px;border-bottom:1px solid #1f2937;background:linear-gradient(135deg,#0ea5e9,#6366f1);">
                <table width="100%">
                  <tr>
                    <td align="left" style="color:#f9fafb;font-size:16px;font-weight:600;">
                      Portfólio · Erik Ingleson
                    </td>
                    <td align="right">
                      {"<img src='" + logo_url + "' alt='Logo' style='max-height:32px;display:block;' />" if logo_url else ""}
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            <tr>
              <td style="padding:24px;">
                <h1 style="margin:0 0 12px;font-size:20px;color:#e5e7eb;">
                  Nova mensagem de contato
                </h1>
                <p style="margin:0 0 16px;font-size:14px;color:#9ca3af;line-height:1.6;">
                  Você recebeu uma nova mensagem pelo formulário de contato do seu portfólio.
                </p>

                <table cellpadding="0" cellspacing="0" style="width:100%;margin-bottom:16px;font-size:14px;color:#e5e7eb;">
                  <tr>
                    <td style="padding:4px 0;width:120px;color:#9ca3af;">Nome:</td>
                    <td style="padding:4px 0;">{name}</td>
                  </tr>
                  <tr>
                    <td style="padding:4px 0;width:120px;color:#9ca3af;">E-mail:</td>
                    <td style="padding:4px 0;">
                      <a href="mailto:{email}" style="color:#38bdf8;text-decoration:none;">{email}</a>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:4px 0;width:120px;color:#9ca3af;">Assunto:</td>
                    <td style="padding:4px 0;">{subject}</td>
                  </tr>
                </table>

                <div style="margin-top:16px;">
                  <p style="margin:0 0 8px;font-size:14px;color:#9ca3af;">Mensagem:</p>
                  <div style="background-color:#020617;border-radius:8px;border:1px solid #1f2937;padding:16px;color:#e5e7eb;font-size:14px;line-height:1.6;white-space:pre-wrap;">
                    {message}
                  </div>
                </div>
              </td>
            </tr>

            <tr>
              <td style="padding:16px 24px;border-top:1px solid #1f2937;text-align:center;font-size:12px;color:#6b7280;">
                Enviado automaticamente pelo portfólio de Erik Ingleson.
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""

            try:
                msg = EmailMultiAlternatives(
                    subject=email_subject,
                    body=text_content,
                    from_email=owner_email,
                    to=[owner_email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except Exception as mail_exc:
                # Se o e-mail falhar, o contato continua salvo
                return api_error(
                    "Mensagem salva, mas houve erro ao enviar o e-mail.",
                    status=500,
                    extra={"detail": str(mail_exc)},
                )

            return JsonResponse(contact_message_to_dict(contact), status=201)

        except Exception as exc:
            return api_error(
                "Erro interno ao enviar mensagem.",
                status=500,
                extra={"detail": str(exc)},
            )



# ---------- Views baseadas em função (listas simples) ----------

@require_http_methods(["GET"])
def portfolio_full(request):
    """
    Retorna todos os dados do portfólio em uma única resposta JSON.
    """
    try:
        profile = UserProfile.objects.first()
        profile_data = user_profile_to_dict(profile) if profile else None

        sections = [
            section_config_to_dict(s)
            for s in SectionConfig.objects.all().order_by("order_index")
        ]
        skills = [
            skill_to_dict(s)
            for s in Skill.objects.all().order_by("order_index", "name")
        ]
        experiences = [
            experience_to_dict(e)
            for e in Experience.objects.all().order_by("order_index", "-start_date")
        ]
        certifications = [
            certification_to_dict(c)
            for c in Certification.objects.all().order_by("order_index", "-issue_date")
        ]
        education_list = [
            education_to_dict(e)
            for e in Education.objects.all().order_by("order_index", "-start_date")
        ]
        services = [
            service_to_dict(s)
            for s in Service.objects.all().order_by("order_index", "title")
        ]
        languages = [
            language_to_dict(l)
            for l in Language.objects.all().order_by("order_index", "name")
        ]
        projects = [
            project_to_dict(p)
            for p in Project.objects.all().order_by("-created_at")
        ]

        data = {
            "profile": profile_data,
            "sections": sections,
            "skills": skills,
            "experiences": experiences,
            "certifications": certifications,
            "education": education_list,
            "services": services,
            "languages": languages,
            "projects": projects,
        }
        return JsonResponse(data, status=200)

    except Exception as exc:
        return api_error(
            "Erro ao carregar dados completos do portfólio.",
            status=500,
            extra={"detail": str(exc)},
        )


@require_http_methods(["GET"])
def profile_detail(request):
    try:
        profile = UserProfile.objects.first()
        if not profile:
            raise Http404("Perfil não encontrado.")
        return JsonResponse(user_profile_to_dict(profile), status=200)
    except Exception as exc:
        return api_error(
            "Erro ao carregar perfil.",
            status=500,
            extra={"detail": str(exc)},
        )


@require_http_methods(["GET"])
def skills_list(request):
    skills = Skill.objects.all().order_by("order_index", "name")
    data = [skill_to_dict(s) for s in skills]
    return JsonResponse(data, status=200, safe=False)


@require_http_methods(["GET"])
def experience_list(request):
    experiences = Experience.objects.all().order_by("order_index", "-start_date")
    data = [experience_to_dict(e) for e in experiences]
    return JsonResponse(data, status=200, safe=False)


@require_http_methods(["GET"])
def certifications_list(request):
    certs = Certification.objects.all().order_by("order_index", "-issue_date")
    data = [certification_to_dict(c) for c in certs]
    return JsonResponse(data, status=200, safe=False)


@require_http_methods(["GET"])
def education_list(request):
    items = Education.objects.all().order_by("order_index", "-start_date")
    data = [education_to_dict(e) for e in items]
    return JsonResponse(data, status=200, safe=False)


@require_http_methods(["GET"])
def services_list(request):
    services = Service.objects.all().order_by("order_index", "title")
    data = [service_to_dict(s) for s in services]
    return JsonResponse(data, status=200, safe=False)


@require_http_methods(["GET"])
def languages_list(request):
    langs = Language.objects.all().order_by("order_index", "name")
    data = [language_to_dict(l) for l in langs]
    return JsonResponse(data, status=200, safe=False)


@require_http_methods(["GET"])
def sections_list(request):
    sections = SectionConfig.objects.all().order_by("order_index")
    data = [section_config_to_dict(s) for s in sections]
    return JsonResponse(data, status=200, safe=False)


@require_http_methods(["GET"])
def projects_list(request):
    """
    Lista todos os projetos. Aceita filtro opcional ?highlight=true
    """
    qs = Project.objects.all().order_by("-created_at")

    highlight = request.GET.get("highlight")
    if highlight is not None:
        if highlight.lower() in ("1", "true", "t", "yes"):
            qs = qs.filter(highlight=True)

    data = [project_to_dict(p) for p in qs]
    return JsonResponse(data, status=200, safe=False)


@require_http_methods(["GET"])
def project_detail(request, slug: str):
    """
    Detalhes de um projeto específico.
    """
    try:
        project = Project.objects.get(slug=slug)
    except Project.DoesNotExist:
        raise Http404("Projeto não encontrado.")

    return JsonResponse(project_to_dict(project), status=200)
