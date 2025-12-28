// app/page.tsx
import Image from "next/image";
import { fetchPortfolio } from "@/lib/api";
import ContactForm from "@/components/ContactForm";

/* ==== Tipos do payload da API ==== */

type SectionConfig = {
  section_key: string;
  is_enabled: boolean;
  order_index: number;
};

type UserProfile = {
  full_name: string;
  job_title: string;
  short_bio: string;
  location: string | null;
  email: string;
  github_url: string | null;
  linkedin_url: string | null;
  avatar_url?: string | null;
};

type Skill = {
  id: number;
  name: string;
  category: string;
  level: string | null;
};

type Experience = {
  id: number;
  company_name: string;
  role: string;
  location: string | null;
  start_date: string;
  end_date: string | null;
  is_current: boolean;
  description: string | null;
};

type Certification = {
  id: number;
  name: string;
  institution: string;
  issue_date: string;
  expiration_date: string | null;
  credential_url: string | null;
};

type EducationItem = {
  id: number;
  institution: string;
  degree: string;
  field_of_study: string | null;
  start_date: string;
  end_date: string | null;
  is_current: boolean;
  description: string | null;
};

type ServiceItem = {
  id: number;
  title: string;
  short_description: string;
};

type LanguageItem = {
  id: number;
  name: string;
  level: string;
};

type Project = {
  id: number;
  title: string;
  short_description: string;
  repo_url: string | null;
  demo_url: string | null;
};

type PortfolioData = {
  profile: UserProfile | null;
  sections: SectionConfig[];
  skills: Skill[];
  experiences: Experience[];
  certifications: Certification[];
  education: EducationItem[];
  services: ServiceItem[];
  languages: LanguageItem[];
  projects: Project[];
};

/* ==== Configuração dos grupos de habilidades (estilo README GitHub) ==== */

const SKILL_GROUPS: { id: string; title: string; items: string[] }[] = [
  {
    id: "languages",
    title: "Linguagens de Programação",
    items: [
      "JavaScript",
      "Python",
      "Java",
      "C#",
      "PL-SQL",
      "HTML5",
      "CSS",
      "EJS",
      "React",
      "Lógica de Programação",
      "C",
      "C++",
      "SQL",
    ],
  },
  {
    id: "frameworks",
    title: "Frameworks",
    items: [
      "Django",
      "Spring Boot",
      "AngularJS",
      "Vue.js",
      "Flask",
      "Spring Batch",
      "JPA",
      "Hibernate",
      "ASP.NET",
      "MVC",
    ],
  },
  {
    id: "tools",
    title: "Ferramentas e Plataformas",
    items: [
      "GitHub",
      "Docker",
      "Kubernetes",
      "Jira",
      "Zabbix",
      "Eclipse",
      "Visual Studio",
      "VS Code",
      "IntelliJ IDEA",
      "Spring Tools",
    ],
  },
  {
    id: "databases",
    title: "Banco de Dados",
    items: [
      "MySQL",
      "Microsoft SQL Server",
      "Postgres",
      "H2 Database",
      "MongoDB",
    ],
  },
  {
    id: "orm",
    title: "ORM",
    items: [
      "SQLAlchemy",
      "Django ORM",
      "Hibernate",
      "Sequelize",
      "TypeORM",
      "Mongoose",
      "Entity Framework",
    ],
  },
  {
    id: "microservices",
    title: "Microserviços",
    items: [".NET MVC", ".NET MVVM"],
  },
  {
    id: "agile",
    title: "Agilidade",
    items: ["Scrum", "Kanban"],
  },
  {
    id: "apis",
    title: "APIs",
    items: [
      "Desenvolvimento de APIs",
      "Integração de APIs",
      "Consumo de APIs",
    ],
  },
  {
    id: "cloud",
    title: "Cloud",
    items: ["AWS", "Azure", "Oracle"],
  },
];

function normalizeSkillName(name: string): string {
  return name.trim().toLowerCase();
}

/* ==== Helpers gerais ==== */

function getInitials(name: string): string {
  const parts = name.split(" ").filter(Boolean);
  return parts
    .slice(0, 2)
    .map((p) => p[0]?.toUpperCase() ?? "")
    .join("");
}

function getGithubUsername(url: string | null): string | null {
  if (!url) return null;
  try {
    const u = new URL(url);
    const segments = u.pathname.split("/").filter(Boolean);
    return segments[0] ?? null;
  } catch {
    return null;
  }
}

export default async function HomePage() {
  const data = (await fetchPortfolio()) as PortfolioData;

  if (!data) {
    return (
      <main style={{ padding: 24 }}>
        <h1>Portfólio indisponível</h1>
        <p>
          A API não respondeu. Verifique a env <b>NEXT_PUBLIC_API_BASE_URL</b> no deploy
          e se o backend está online.
        </p>
      </main>
    );
  }

  const {
  profile = null,
  sections = [],
  skills = [],
  experiences = [],
  certifications = [],
  education = [],
  services = [],
  languages = [],
  projects = [],
} = data ?? {};

  const isSectionEnabled = (key: string): boolean =>
    sections.some(
      (section) => section.section_key === key && section.is_enabled
    );

  const githubUsername = getGithubUsername(profile?.github_url ?? null);

  // ✅ Links fixos
  const linkedinUrl =
    "https://www.linkedin.com/in/erik-ingleson-amaral-arruda-b730ba157/";
  const whatsappUrl = "https://wa.me/5511930904071";
  const cvUrl = "/cv/erik-ingleson-cv.pdf";

  // ✅ Foto do Erik (fallback pro arquivo local)
  const avatarSrc = profile?.avatar_url ?? "/images/erik-avatar.jpg";

  // ✅ Normaliza nomes estáticos para saber o que é "extra" vindo do backend
  const staticSkillNames = new Set(
    SKILL_GROUPS.flatMap((group) =>
      group.items.map((item) => normalizeSkillName(item))
    )
  );

  const extraSkills = skills.filter(
    (skill) => !staticSkillNames.has(normalizeSkillName(skill.name))
  );

  return (
    <main className="portfolio-page">
      {/* NAVBAR FIXA */}
      <header className="top-nav">
        <div className="top-nav-shell">
          <span className="top-nav-logo">
            Erik Ingleson · Software Engineer
          </span>
          <nav className="top-nav-links">
            <a href="#sobre">Sobre</a>
            <a href="#habilidades">Habilidades</a>
            <a href="#experiencia">Experiência</a>
            <a href="#projetos">Projetos</a>
            <a href="#contato">Contato</a>
          </nav>
        </div>
      </header>

      <div className="portfolio-shell">
        <div className="portfolio-layout">
          {/* COLUNA ESQUERDA - SIDEBAR */}
          {profile && (
            <aside className="profile-column">
              <div className="profile-card">
                <div className="profile-avatar">
                  {avatarSrc ? (
                    <Image
                      src={avatarSrc}
                      alt={profile.full_name}
                      width={200}
                      height={200}
                      className="profile-avatar-img"
                    />
                  ) : (
                    <span className="profile-avatar-initial">
                      {getInitials(profile.full_name)}
                    </span>
                  )}
                </div>

                <h1 className="profile-name">{profile.full_name}</h1>

                {githubUsername && (
                  <p className="profile-username">{githubUsername}</p>
                )}

                <p className="profile-role">{profile.job_title}</p>

                <p className="profile-mini-bio">{profile.short_bio}</p>

                <div className="profile-meta">
                  {profile.location && (
                    <div className="profile-meta-row">
                      <span className="profile-meta-label">Localização</span>
                      <span>{profile.location}</span>
                    </div>
                  )}
                  <div className="profile-meta-row">
                    <span className="profile-meta-label">E-mail</span>
                    <a
                      href={`mailto:${profile.email}`}
                      className="profile-meta-link"
                    >
                      {profile.email}
                    </a>
                  </div>
                </div>

                <div className="profile-links">
                  {profile.github_url && (
                    <a
                      href={profile.github_url}
                      target="_blank"
                      rel="noreferrer"
                      className="profile-link-button"
                    >
                      🐙 GitHub
                    </a>
                  )}
                  {linkedinUrl && (
                    <a
                      href={linkedinUrl}
                      target="_blank"
                      rel="noreferrer"
                      className="profile-link-button secondary"
                    >
                      🔗 LinkedIn
                    </a>
                  )}
                </div>
              </div>
            </aside>
          )}

          {/* COLUNA DIREITA - CONTEÚDO PRINCIPAL */}
          <section className="content-column">
            {/* HERO / CAPA ILUSTRADA */}
            {profile && isSectionEnabled("hero") && (
              <section id="sobre" className="hero-banner">
                <div className="hero-banner-inner">
                  <div className="hero-banner-left">
                    <p className="hero-banner-kicker">
                      Portfólio · Software Engineer
                    </p>
                    <h2 className="hero-banner-title">
                      {profile.full_name}
                    </h2>
                    <p className="hero-banner-subtitle">
                      {profile.job_title}
                    </p>
                    <p className="hero-banner-text">
                      {profile.short_bio}
                    </p>

                    <div className="hero-banner-meta">
                      {profile.location && (
                        <span className="hero-banner-pill">
                          {profile.location}
                        </span>
                      )}
                      <span className="hero-banner-pill">
                        <a href={`mailto:${profile.email}`}>
                          {profile.email}
                        </a>
                      </span>
                      {githubUsername && (
                        <span className="hero-banner-pill">
                          @{githubUsername}
                        </span>
                      )}
                    </div>

                    <div className="hero-cta-row">
                      <a
                        href={cvUrl}
                        className="hero-cta hero-cta-primary"
                      >
                        📄 Baixar CV
                      </a>
                      <a
                        href={whatsappUrl}
                        target="_blank"
                        rel="noreferrer"
                        className="hero-cta hero-cta-secondary"
                      >
                        💬 Falar no WhatsApp
                      </a>
                    </div>
                  </div>

                  {/* Ilustração abstrata */}
                  <div className="hero-banner-right">
                    <div className="hero-orbit hero-orbit-1" />
                    <div className="hero-orbit hero-orbit-2" />
                    <div className="hero-orbit hero-orbit-3" />
                  </div>
                </div>
              </section>
            )}

            {/* HABILIDADES - ESTILO README GITHUB */}
            {isSectionEnabled("skills") && (
              <section id="habilidades" className="card-section">
                <h2 className="card-title">Habilidades</h2>

                {SKILL_GROUPS.map((group) => (
                  <div key={group.id} className="skills-block">
                    <h3 className="skills-category">{group.title}</h3>
                    <div className="badge-row">
                      {group.items.map((item) => (
                        <span
                          key={item}
                          className={`badge badge-group-${group.id}`}
                        >
                          {item}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}

                {extraSkills.length > 0 && (
                  <div className="skills-block">
                    <h3 className="skills-category">Outras tecnologias</h3>
                    <div className="badge-row">
                      {extraSkills.map((skill) => (
                        <span
                          key={skill.id}
                          className="badge badge-group-other"
                        >
                          {skill.name}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </section>
            )}

            {/* EXPERIÊNCIA */}
            {isSectionEnabled("experience") && experiences.length > 0 && (
              <section id="experiencia" className="card-section">
                <h2 className="card-title">Experiência</h2>
                <ul className="timeline-list">
                  {experiences.map((exp) => (
                    <li key={exp.id} className="timeline-item">
                      <div className="timeline-dot" />
                      <div className="timeline-content">
                        <div className="timeline-header">
                          <span className="timeline-role">{exp.role}</span>
                          <span className="timeline-company">
                            · {exp.company_name}
                          </span>
                        </div>
                        <div className="timeline-meta">
                          {exp.location && (
                            <span>{exp.location} · </span>
                          )}
                          <span>
                            {exp.start_date} —{" "}
                            {exp.is_current ? "Atual" : exp.end_date || ""}
                          </span>
                        </div>
                        {exp.description && (
                          <p className="timeline-description">
                            {exp.description}
                          </p>
                        )}
                      </div>
                    </li>
                  ))}
                </ul>
              </section>
            )}

            {/* PROJETOS */}
            {isSectionEnabled("projects") && projects.length > 0 && (
              <section id="projetos" className="card-section">
                <h2 className="card-title">Projetos em destaque</h2>
                <div className="projects-grid">
                  {projects.map((project) => (
                    <article key={project.id} className="project-card">
                      <h3 className="project-title">{project.title}</h3>
                      <p className="project-description">
                        {project.short_description}
                      </p>
                      <div className="project-links">
                        {project.repo_url && (
                          <a
                            href={project.repo_url}
                            target="_blank"
                            rel="noreferrer"
                            className="project-link"
                          >
                            Código
                          </a>
                        )}
                        {project.demo_url && (
                          <a
                            href={project.demo_url}
                            target="_blank"
                            rel="noreferrer"
                            className="project-link"
                          >
                            Demo
                          </a>
                        )}
                      </div>
                    </article>
                  ))}
                </div>
              </section>
            )}

            {/* FORMAÇÃO */}
            {isSectionEnabled("education") && education.length > 0 && (
              <section className="card-section">
                <h2 className="card-title">Formação</h2>
                <ul className="simple-list">
                  {education.map((edu) => (
                    <li key={edu.id} className="simple-item">
                      <span className="simple-main">
                        {edu.degree} · {edu.institution}
                      </span>
                      <span className="simple-sub">
                        {edu.start_date} —{" "}
                        {edu.is_current ? "Cursando" : edu.end_date || ""}
                      </span>
                      {edu.field_of_study && (
                        <span className="simple-extra">
                          {edu.field_of_study}
                        </span>
                      )}
                    </li>
                  ))}
                </ul>
              </section>
            )}

            {/* CERTIFICAÇÕES */}
            {isSectionEnabled("certifications") &&
              certifications.length > 0 && (
                <section className="card-section">
                  <h2 className="card-title">Certificações</h2>
                  <ul className="simple-list">
                    {certifications.map((cert) => (
                      <li key={cert.id} className="simple-item">
                        <span className="simple-main">
                          {cert.name} · {cert.institution}
                        </span>
                        <span className="simple-sub">
                          Emitido em {cert.issue_date}
                        </span>
                        {cert.credential_url && (
                          <a
                            href={cert.credential_url}
                            target="_blank"
                            rel="noreferrer"
                            className="simple-link"
                          >
                            Ver certificado
                          </a>
                        )}
                      </li>
                    ))}
                  </ul>
                </section>
              )}

            {/* SERVIÇOS */}
            {isSectionEnabled("services") && services.length > 0 && (
              <section className="card-section">
                <h2 className="card-title">Serviços</h2>
                <ul className="simple-list">
                  {services.map((svc) => (
                    <li key={svc.id} className="simple-item">
                      <span className="simple-main">{svc.title}</span>
                      <span className="simple-sub">
                        {svc.short_description}
                      </span>
                    </li>
                  ))}
                </ul>
              </section>
            )}

            {/* IDIOMAS */}
            {isSectionEnabled("languages") && languages.length > 0 && (
              <section className="card-section">
                <h2 className="card-title">Idiomas</h2>
                <ul className="simple-list">
                  {languages.map((lang) => (
                    <li key={lang.id} className="simple-item">
                      <span className="simple-main">
                        {lang.name} — {lang.level}
                      </span>
                    </li>
                  ))}
                </ul>
              </section>
            )}

            {/* CONTATO */}
            {isSectionEnabled("contact") && (
              <section id="contato" className="card-section">
                <h2 className="card-title">Contato</h2>
                <p className="card-muted">
                  Me envie uma mensagem e retornarei assim que possível.
                </p>
                <ContactForm />
              </section>
            )}
          </section>
        </div>
      </div>
    </main>
  );
}
