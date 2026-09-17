from app.models import Job
from app.job_repository import JobRepository

job_json_path = r"D:\Projects\AI-Job-Hunter\data\job.json"
repository = JobRepository(job_json_path)

def test_get_all_jobs():
    jobs = repository.get_all()
    assert len(jobs) == 5
    assert all(isinstance(job, Job) for job in jobs)

def test_get_existing_job():
    job = repository.get_by_id("job_003")
    assert job is not None
    assert job.job_id == "job_003"

def test_missing_job():
    job = repository.get_by_id("job_999")
    assert job is None