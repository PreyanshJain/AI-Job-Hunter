from datetime import datetime
from pydantic import ValidationError
from app.models import Job, Resume, Application
from app.storage import save_json, load_json

job_1 = Job(
    job_id= "job_001",
    title="AI Engineer",
    company="Microsoft",
    location="Hyderabad",
    url="https://example.com/job",
    description="Looking for an AI Engineer...",
    skills=["Python", "LangChain", "RAG"],
    experience="2-4 years",
    source="LinkedIn"
)

job_2 = Job(
    job_id= "job_002",
    title="AI Engineer",
    company="Microsoft",
    location="Hyderabad",
    url="https://example.com/job",
    description="Looking for an AI Engineer...",
    skills=["Python", "LangChain", "RAG"],
    experience="2-4 years",
    source="LinkedIn"
)

job = [job_1, job_2]


resume = Resume(
    name="Candidate",
    summary="Python developer transitioning into AI Engineering",
    education=["B.Tech in Computer Science"],
    experience=["Python Developer at Infosys"],
    projects=["AI Job Hunter"],
    skills=["Python", "SQL", "LangChain"],
    certifications=["Generative AI Certification"]
)

application = Application(
    job_id = "job_001",
    resume_version = "master_v1",
    match_score = 82,
    ats_score = 76,
    status = "saved",
    applied_at = datetime(2026, 8, 20, 2, 58, 0),
    notes = "Good match for Python + GenAI"
)

job_json_path = r"D:\Projects\AI-Job-Hunter\data\job.json"
resume_json_path = r"D:\Projects\AI-Job-Hunter\data\resume.json"
application_json_path = r"D:\Projects\AI-Job-Hunter\data\application.json"

save_json(job, job_json_path)
save_json(resume, resume_json_path)
save_json(application, application_json_path)

job_data = load_json(job_json_path)
resume_data = load_json(resume_json_path)
application_data = load_json(application_json_path)

job_model = [Job.model_validate(i) for i in job_data]
try:
    resume_model = Resume.model_validate(resume_data)
except ValidationError as e:
    print(f"Error: {e}")
application_model = Application.model_validate(application_data)

