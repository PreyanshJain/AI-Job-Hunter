from app.models import Job
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
    loaded_job =Job.model_validate(json_data)

    assert original_job == loaded_job
