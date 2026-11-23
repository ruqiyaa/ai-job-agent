
import re
from datetime import datetime
import hashlib


# Skills we know how to identify in job descriptions
SKILL_ALIASES = {
    "Python": ["python"],
    "JavaScript": ["javascript", "js"],
    "React.js": ["react.js", "reactjs", "react"],
    "HTML5": ["html5", "html"],
    "CSS3": ["css3", "css"],
    "Redux": ["redux"],
    "REST APIs": ["rest api", "rest apis"],
    "Git": ["git"],
    "Flask": ["flask"],
    "Django": ["django"],
    "FastAPI": ["fastapi"],
    "SQL": ["sql", "mysql", "postgresql"],
    "Docker": ["docker"],
    "Vue.js": ["vue.js", "vuejs", "vue"],
    "Node.js": ["node.js", "nodejs"],
    "TypeScript": ["typescript"],
    "ERPNext": ["erpnext"],
    "Frappe": ["frappe"],
    "AWS": ["aws"],
    "CI/CD": ["ci/cd"],
    "Data Structures": ["data structures"],
    "Automation": ["automation"],
    "HTML": ["html"],
}


def contains_term(text, term):
    pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"
    return bool(re.search(pattern, text, re.IGNORECASE))


def extract_skills(text):
    found = set()
    text = text or ""

    for skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            if contains_term(text, alias):
                found.add(skill)
                break

    return found


def get_candidate_years(experience):
    """Estimate years from a resume experience field."""

    text = experience.lower()

    # Example: 3 years of experience
    match = re.search(r"(\d+(?:\.\d+)?)\s*\+?\s*years?", text)

    if match:
        return float(match.group(1))

    # Example: Frontend Developer | 2023–2026
    match = re.search(
        r"(20\d{2})\s*[-–—]\s*(present|current|20\d{2})",
        text,
        re.IGNORECASE
    )

    if match:
        start_year = int(match.group(1))
        end_value = match.group(2)

        end_year = (
            datetime.now().year
            if end_value.lower() in ["present", "current"]
            else int(end_value)
        )

        return max(0, end_year - start_year)

    return None


def get_required_years(description):
    """Find experience requirements in a job description."""

    text = description.lower()

    if "fresher" in text or "fresh graduate" in text:
        return 0, 0

    # Example: 4-5 years, 4–5 years
    match = re.search(
        r"(\d+)\s*[-–—to]+\s*(\d+)\s*\+?\s*years?",
        text
    )

    if match:
        return int(match.group(1)), int(match.group(2))

    # Example: 8 years, 5+ years
    match = re.search(r"(\d+)\s*\+?\s*years?", text)

    if match:
        years = int(match.group(1))
        return years, years

    return None, None


def extract_job_skill_levels(job):
    """Classify job skills as required, preferred, or simply mentioned."""

    description = job.get("description") or ""
    title = job.get("title") or ""

    required = extract_skills(title)
    preferred = set()
    mentioned = set()

    optional_words = [
        "preferred",
        "nice to have",
        "good to have",
        "desirable",
        "bonus",
        "an advantage"
    ]

    required_words = [
        "required",
        "must have",
        "mandatory",
        "essential",
        "proficient in",
        "experience with",
        "experience in",
        "strong knowledge of",
        "hands-on experience"
    ]

    sentences = re.split(r"[.!?;\n]+", description)

    for sentence in sentences:
        sentence_skills = extract_skills(sentence)
        sentence_lower = sentence.lower()

        if any(word in sentence_lower for word in optional_words):
            preferred.update(sentence_skills)

        elif any(word in sentence_lower for word in required_words):
            required.update(sentence_skills)

        else:
            mentioned.update(sentence_skills)

    # Required takes priority if a skill appears in multiple categories.
    preferred -= required
    mentioned -= required
    mentioned -= preferred

    return required, preferred, mentioned


def score_skills(candidate_skills, job):
    required, preferred, mentioned = extract_job_skill_levels(job)

    matched_required = candidate_skills & required
    missing_required = required - candidate_skills

    matched_preferred = candidate_skills & preferred
    missing_preferred = preferred - candidate_skills

    matched_mentioned = candidate_skills & mentioned

    # Required skills matter most.
    total_weight = (
        len(required) * 3
        + len(preferred)
        + len(mentioned)
    )

    matched_weight = (
        len(matched_required) * 3
        + len(matched_preferred)
        + len(matched_mentioned)
    )

    if total_weight == 0:
        return 25, [], [], []

    score = round((matched_weight / total_weight) * 50)

    matched = sorted(
        matched_required | matched_preferred | matched_mentioned
    )

    return (
        score,
        matched,
        sorted(missing_required),
        sorted(missing_preferred)
    )


def score_experience(candidate_years, candidate_titles, job):
    """Score experience based on how relevant the candidate's role is."""

    description = job.get("description") or ""
    job_title = job.get("title") or ""

    minimum, maximum = get_required_years(description)

    if minimum is None:
        base_score = 24
    elif candidate_years is None:
        base_score = 12
    elif minimum == 0:
        base_score = 30 if candidate_years <= 1 else 15
    elif candidate_years < minimum:
        base_score = round(30 * candidate_years / minimum)
    elif candidate_years <= maximum:
        base_score = 30
    else:
        base_score = 27

    # Compare the candidate's current role with the job role.
    candidate_text = " ".join(candidate_titles).lower()
    job_text = job_title.lower()

    frontend_terms = ["frontend", "front-end", "ui developer"]
    backend_terms = ["backend", "back-end", "python developer"]

    candidate_is_frontend = any(
        term in candidate_text for term in frontend_terms
    )
    job_is_backend = any(
        term in job_text for term in backend_terms
    )

    # Frontend experience is transferable, but isn't Python experience.
    if candidate_is_frontend and job_is_backend:
        return round(base_score * 0.2)

    return base_score


def score_role(candidate_titles, job_title, matched_skills):
    """Measure role similarity and transferable technical skills."""

    candidate_text = " ".join(candidate_titles).lower()
    job_text = job_title.lower()

    frontend_terms = ["frontend", "front-end", "ui developer"]
    backend_terms = ["backend", "back-end", "python developer"]

    candidate_frontend = any(
        term in candidate_text for term in frontend_terms
    )

    candidate_backend = any(
        term in candidate_text for term in backend_terms
    )

    job_frontend = any(
        term in job_text for term in frontend_terms
    )

    job_backend = any(
        term in job_text for term in backend_terms
    )

    if candidate_frontend and job_frontend:
        base_score = 15
    elif candidate_backend and job_backend:
        base_score = 15
    elif candidate_frontend and job_backend:
        base_score = 5
    else:
        base_score = 10

    # Reward transferable technical skills.
    transferable_skills = {
        "React.js",
        "JavaScript",
        "REST APIs",
        "HTML5",
        "CSS3",
        "Git"
    }

    overlap = len(set(matched_skills) & transferable_skills)

    bonus = min(overlap, 5)

    return min(base_score + bonus, 15)


def score_education(candidate_education, description):
    description = description.lower()
    education_text = " ".join(candidate_education).lower()

    degree_terms = [
        "b.tech",
        "bachelor",
        "computer science",
        "computer engineering",
        "master",
        "degree"
    ]

    required_education = [
        term for term in degree_terms
        if term in description
    ]

    if not required_education:
        return 5

    if any(term in education_text for term in required_education):
        return 5

    return 1


def remove_duplicate_jobs(jobs):
    """Remove jobs with identical title, company and description."""

    unique_jobs = []
    seen = set()

    for job in jobs:
        title = (job.get("title") or "").strip().lower()
        company = (job.get("company") or "").strip().lower()
        description = (job.get("description") or "").strip().lower()

        content = f"{title}|{company}|{description}"

        fingerprint = hashlib.sha256(
            content.encode("utf-8")
        ).hexdigest()

        if fingerprint not in seen:
            seen.add(fingerprint)
            unique_jobs.append(job)

    return unique_jobs


def match_jobs(candidate_profile, jobs):
    candidate_skills = {
        skill.lower()
        for skill in candidate_profile.get("skills", [])
    }

    # Normalize candidate skills using the same skill catalog.
    normalized_skills = extract_skills(
        " ".join(candidate_skills)
    )

    candidate_years = get_candidate_years(
        candidate_profile.get("experience", "")
    )

    candidate_titles = candidate_profile.get("job_titles", [])
    results = []

    unique_jobs = remove_duplicate_jobs(jobs)

    for job in unique_jobs[:10]:

        skill_score, matched, missing, optional_missing = score_skills(
            normalized_skills,
            job
        )

        experience_score = score_experience(
            candidate_years,
            candidate_titles,
            job
        )

        role_score = score_role(
            candidate_titles,
            job.get("title") or "",
            matched
        )

        education_score = score_education(
            candidate_profile.get("education", []),
            job.get("description") or ""
        )

        final_score = (
            skill_score
            + experience_score
            + role_score
            + education_score
        )

        if missing:
            skill_explanation = (
                "Missing relevant skills: " + ", ".join(missing) + "."
            )
        else:
            skill_explanation = "All detected job skills are matched."

        explanation = (
            f"Skills: {skill_score}/50. "
            f"Experience: {experience_score}/30. "
            f"Role relevance: {role_score}/15. "
            f"Education: {education_score}/5. "
            f"{skill_explanation}"
        )

        results.append({
            "job_id": job["id"],
            "title": job["title"],
            "company": job["company"],
            "match_score": final_score,
            "matched_skills": matched,
            "missing_skills": missing,
            "optional_missing_skills": optional_missing,
            "candidate_experience_years": candidate_years,
            "score_breakdown": {
                "skills": skill_score,
                "experience": experience_score,
                "role_relevance": role_score,
                "education": education_score
            },
            "explanation": explanation
        })

    return sorted(
        results,
        key=lambda item: item["match_score"],
        reverse=True
    )
