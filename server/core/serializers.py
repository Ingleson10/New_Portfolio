# core/serializers.py
from typing import Dict
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


def user_profile_to_dict(profile: UserProfile) -> Dict:
    return {
        "id": profile.id,
        "full_name": profile.full_name,
        "job_title": profile.job_title,
        "short_bio": profile.short_bio,
        "location": profile.location,
        "email": profile.email,
        "phone": profile.phone,
        "github_url": profile.github_url,
        "linkedin_url": profile.linkedin_url,
        "portfolio_slug": profile.portfolio_slug,
    }


def skill_to_dict(skill: Skill) -> Dict:
    return {
        "id": skill.id,
        "name": skill.name,
        "category": skill.category,
        "level": skill.level,
        "icon_key": skill.icon_key,
        "order_index": skill.order_index,
    }


def experience_to_dict(exp: Experience) -> Dict:
    return {
        "id": exp.id,
        "company_name": exp.company_name,
        "role": exp.role,
        "location": exp.location,
        "start_date": exp.start_date.isoformat(),
        "end_date": exp.end_date.isoformat() if exp.end_date else None,
        "is_current": exp.is_current,
        "description": exp.description,
        "order_index": exp.order_index,
    }


def certification_to_dict(cert: Certification) -> Dict:
    return {
        "id": cert.id,
        "name": cert.name,
        "institution": cert.institution,
        "issue_date": cert.issue_date.isoformat(),
        "expiration_date": cert.expiration_date.isoformat()
        if cert.expiration_date
        else None,
        "credential_id": cert.credential_id,
        "credential_url": cert.credential_url,
        "order_index": cert.order_index,
    }


def project_to_dict(project: Project) -> Dict:
    return {
        "id": project.id,
        "title": project.title,
        "slug": project.slug,
        "short_description": project.short_description,
        "long_description": project.long_description,
        "repo_url": project.repo_url,
        "demo_url": project.demo_url,
        "highlight": project.highlight,
        "created_at": project.created_at.isoformat() if project.created_at else None,
        "updated_at": project.updated_at.isoformat() if project.updated_at else None,
    }


def education_to_dict(edu: Education) -> Dict:
    return {
        "id": edu.id,
        "institution": edu.institution,
        "degree": edu.degree,
        "field_of_study": edu.field_of_study,
        "start_date": edu.start_date.isoformat(),
        "end_date": edu.end_date.isoformat() if edu.end_date else None,
        "is_current": edu.is_current,
        "description": edu.description,
        "order_index": edu.order_index,
    }


def service_to_dict(svc: Service) -> Dict:
    return {
        "id": svc.id,
        "title": svc.title,
        "short_description": svc.short_description,
        "detailed_description": svc.detailed_description,
        "icon_key": svc.icon_key,
        "highlight": svc.highlight,
        "order_index": svc.order_index,
    }


def language_to_dict(lang: Language) -> Dict:
    return {
        "id": lang.id,
        "name": lang.name,
        "level": lang.level,
        "order_index": lang.order_index,
    }


def section_config_to_dict(section: SectionConfig) -> Dict:
    return {
        "id": section.id,
        "section_key": section.section_key,
        "is_enabled": section.is_enabled,
        "order_index": section.order_index,
    }


def contact_message_to_dict(msg: ContactMessage) -> Dict:
    return {
        "id": msg.id,
        "name": msg.name,
        "email": msg.email,
        "subject": msg.subject,
        "message": msg.message,
        "created_at": msg.created_at.isoformat() if msg.created_at else None,
        "is_read": msg.is_read,
    }
