from pydantic import ValidationError
from app.models import Resume
from app.job_repository import JobRepository
from app.storage import save_json, load_json
from app.pdf_extractor import extract_text
from app.job_processor import process_job
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

except ValidationError as error:
    print("Resume validation failed:")
    print(error)

repository = JobRepository(job_json_path)
jobs = repository.get_all()
for job in jobs:
    processed_job = process_job(job)
    processed_job_dict = {
        "job_id": processed_job.job_id,
        "skills": processed_job.skills,
        "experience": processed_job.experience,
        "responsibilities": processed_job.responsibilities,
        "education": processed_job.education,
        "keywords": processed_job.keywords,
    }
    print(processed_job_dict)