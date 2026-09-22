from pydantic import ValidationError
from app.models import Resume, MatchResult
from app.job_repository import JobRepository
from app.storage import save_json, load_json
from app.pdf_extractor import extract_text
from app.job_processor import process_job
from app.matching_engine import extract_resume_skills, match_skills, calculate_match_score
from app.resume_parser import (
    parse_resume,
    parse_education,
    parse_experience,
    parse_projects,
    parse_skills,
    combine_bullet_lines,
)


job_json_path = r"D:\Projects\AI-Job-Hunter\data\job.json"
resume_json_path = r"D:\Projects\AI-Job-Hunter\data\resume.json"
application_json_path = r"D:\Projects\AI-Job-Hunter\data\application.json"

resume_path = r"D:\Projects\AI-Job-Hunter\documents\Preyansh_Jain_AI_Engineer_Resume_2.pdf"
text, personal_details = extract_text(resume_path)
if not text:
    print("Resume extraction failed!")
    exit()
try:
    sections = parse_resume(text)
    sections["personal_details"] = personal_details
    sections["education"] = parse_education(sections["education"])
    sections["experience"] = parse_experience(sections["experience"])
    sections["projects"] = parse_projects(sections.get("projects", []))
    sections["skills"] = parse_skills(sections["skills"])
    sections["certifications"] = combine_bullet_lines(sections.get("certifications", []))
    sections["internships"] = parse_experience(sections.get("internships", []))
    sections["achievements"] = combine_bullet_lines(sections.get("achievements", []))
    resume = Resume.model_validate(sections)
    save_json(resume, resume_json_path)
    loaded_data = load_json(resume_json_path)
    loaded_resume = Resume.model_validate(loaded_data)
    resume_skills = extract_resume_skills(loaded_resume)

except ValidationError as error:
    print("Resume validation failed:")
    print(error)
    raise

repository = JobRepository(job_json_path)
jobs = repository.get_all()
match_results = []
for job in jobs:
    processed_job = process_job(job)
    matched_skills, missing_skills = match_skills(resume_skills, processed_job.skills)
    score = calculate_match_score(matched_skills,  processed_job.skills)
    match_results.append(MatchResult(
            job_id=processed_job.job_id,
            match_score=score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
        )
    )
print(match_results)