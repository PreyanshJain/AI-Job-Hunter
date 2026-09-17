import pytest
from pydantic import ValidationError
from app.models import Job
from app.storage import save_json, load_json
from app.job_loader import load_jobs


def test_load_jobs(tmp_path):
    original_job_1 = Job(
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
    original_job_2 = Job(
        job_id="job_002",
        title="GenAI Engineer",
        company="Microsoft",
        location="Bangalore",
        url="https://www.microsoft.com/",
        description= "Looking for a GenAI Engineer with experience building LLM applications using OpenAI, LangChain, vector databases and Azure.",
        skills=["Python","OpenAI","LangChain","Vector Database","Azure"],
        experience="3-5 years",
        source="LinkedIn"
    )

    original_job = [original_job_1, original_job_2]
    file_path = tmp_path / "jobs.json"
    save_json(original_job, file_path)
    loaded_jobs = load_jobs(file_path)

    assert len(loaded_jobs) == 2
    assert original_job_1 == loaded_jobs[0]
    assert original_job_2 == loaded_jobs[1]
    assert original_job == loaded_jobs
    assert all(isinstance(job, Job) for job in loaded_jobs)


def test_invalid_job_data(tmp_path):
    original_job_1 = Job(
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
    original_job_2 = Job(
        job_id="job_002",
        title="GenAI Engineer",
        company="Microsoft",
        location="Bangalore",
        url="https://www.microsoft.com/",
        description= "Looking for a GenAI Engineer with experience building LLM applications using OpenAI, LangChain, vector databases and Azure.",
        skills=["Python","OpenAI","LangChain","Vector Database","Azure"],
        experience="3-5 years",
        source="LinkedIn"
    )

    original_job = [original_job_1, original_job_2]
    file_path = tmp_path / "jobs.json"
    save_json(original_job, file_path)
    job_data = load_json(file_path)
    del job_data[0]['title']
    with pytest.raises(ValidationError):
        [Job.model_validate(job) for job in job_data]