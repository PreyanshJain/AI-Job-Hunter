from app.storage import load_json
from app.models import Job


def load_jobs(file_path):
    job_data = load_json(file_path)
    jobs = [Job.model_validate(job) for job in job_data]
    return jobs