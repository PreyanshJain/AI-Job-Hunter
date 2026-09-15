from app.models import Job, Resume
from app.storage import save_json, load_json

def test_save_and_load_job(tmp_path):
    original_job = Job(
        job_id="job_001",
        title="AI Engineer",
        company="Microsoft",
        location="Hyderabad",
        url="https://example.com/job",
        description="Looking for an AI Engineer...",
        skills=["Python", "LangChain", "RAG"],
        experience="2-4 years",
        source="LinkedIn"
    )
    file_path = tmp_path/"job.json"
    save_json(original_job, file_path)
    json_data = load_json(file_path)
    loaded_job = Job.model_validate(json_data)

    assert original_job == loaded_job


def test_save_and_load_resume(tmp_path):
    original_resume = Resume(
        personal_details= {"name": "Test User", "email": "test@example.com", "phone_number": "1234567890", "linkedin": "", "github": ""},
        summary="Python developer with AI experience.",
        education=[{"institution": "Test University", "degree": "B.E.", "start_date": "2017",  "end_date": "2021", "location": "Indore", "cgpa": "8.0/10"}],
        experience=[{"company": "Test Company", "role": "Python Developer", "start_date": "2021", "end_date": "Present",  "location": "Pune", "responsibilities": ["Developed Python applications.", "Worked with SQL databases."]}],
        projects=[{"project_name": "Test Project", "project_description": ["Built a Python application."], "technologies": ["Python", "SQL"]}],
        internships=[],
        skills=[{"category": "Programming", "skills": ["Python", "SQL"]}],
        certifications=[],
        achievements=[]
    )
    file_path = tmp_path / "resume.json"
    save_json(original_resume, file_path)
    json_data = load_json(file_path)
    loaded_resume = Resume.model_validate(json_data)
    assert original_resume == loaded_resume