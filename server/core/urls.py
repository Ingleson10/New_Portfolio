# core/urls.py
from django.urls import path
from .views import (
    profile_detail,
    skills_list,
    experience_list,
    certifications_list,
    education_list,
    services_list,
    languages_list,
    sections_list,
    projects_list,
    project_detail,
    portfolio_full,      # <- aqui está certo
    ContactCreateView,   # pode importar aqui junto também
)

urlpatterns = [
    path("profile/", profile_detail),
    path("skills/", skills_list),
    path("experience/", experience_list),
    path("certifications/", certifications_list),
    path("education/", education_list),
    path("services/", services_list),
    path("languages/", languages_list),
    path("sections/", sections_list),
    path("projects/", projects_list),
    path("projects/<slug:slug>/", project_detail),
    path("contact/", ContactCreateView.as_view()),
    path("portfolio/", portfolio_full, name="api-portfolio-full"),
]
