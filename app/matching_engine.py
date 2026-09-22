from app.models import Resume
from app.job_processor import normalize_text

def extract_resume_skills(resume: Resume) -> list[str]:
    return [normalize_text(skill) for category in resume.skills for skill in category.skills]


def match_skills(resume_skills: list[str], job_skills: list[str]) -> tuple[list[str], list[str]]:
    matched_skills = []
    missing_skills = []
    for skill in job_skills:
        if skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)
    return matched_skills, missing_skills

def calculate_match_score(matched_skills: list[str], job_skills: list[str]) -> float:
    if not job_skills:
        return 0.0
    return round(len(matched_skills) / len(job_skills) * 100, 2)