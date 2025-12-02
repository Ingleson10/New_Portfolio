// lib/api.ts

const BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

export interface PortfolioProfile {
  id: number;
  full_name: string;
  job_title: string;
  short_bio: string;
  location: string | null;
  email: string;
  phone: string | null;
  github_url: string | null;
  linkedin_url: string | null;
  portfolio_slug: string;
}

export interface SectionConfig {
  id: number;
  section_key: string;
  is_enabled: boolean;
  order_index: number;
}

export interface Skill {
  id: number;
  name: string;
  category: string;
  level: string | null;
  icon_key: string | null;
  order_index: number;
}

export interface Experience {
  id: number;
  company_name: string;
  role: string;
  location: string | null;
  start_date: string;
  end_date: string | null;
  is_current: boolean;
  description: string | null;
  order_index: number;
}

export interface Certification {
  id: number;
  name: string;
  institution: string;
  issue_date: string;
  expiration_date: string | null;
  credential_id: string | null;
  credential_url: string | null;
  order_index: number;
}

export interface Education {
  id: number;
  institution: string;
  degree: string;
  field_of_study: string | null;
  start_date: string;
  end_date: string | null;
  is_current: boolean;
  description: string | null;
  order_index: number;
}

export interface Service {
  id: number;
  title: string;
  short_description: string;
  detailed_description: string | null;
  icon_key: string | null;
  highlight: boolean;
  order_index: number;
}

export interface Language {
  id: number;
  name: string;
  level: string;
  order_index: number;
}

export interface Project {
  id: number;
  title: string;
  slug: string;
  short_description: string;
  long_description: string | null;
  repo_url: string | null;
  demo_url: string | null;
  highlight: boolean;
  created_at: string | null;
  updated_at: string | null;
}

export interface PortfolioResponse {
  profile: PortfolioProfile | null;
  sections: SectionConfig[];
  skills: Skill[];
  experiences: Experience[];
  certifications: Certification[];
  education: Education[];
  services: Service[];
  languages: Language[];
  projects: Project[];
}

export async function fetchPortfolio(): Promise<PortfolioResponse> {
  const res = await fetch(`${BASE_URL}/api/portfolio/`, {
    cache: "no-store", // sempre dados atualizados
  });

  if (!res.ok) {
    throw new Error(`Erro ao buscar portfólio: ${res.status}`);
  }

  return res.json();
}

export async function sendContactMessage(payload: {
  name: string;
  email: string;
  subject: string;
  message: string;
}) {
  const res = await fetch(`${BASE_URL}/api/contact/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const errorBody = await res.json().catch(() => ({}));
    throw new Error(errorBody.error || "Erro ao enviar mensagem de contato.");
  }

  return res.json();
}
