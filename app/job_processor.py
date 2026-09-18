from app.models import Job, ProcessedJob


def normalize_text(text):
    return text.lower().strip()


def process_job(job:Job) -> ProcessedJob:
    job_id = job.job_id
    skills = [normalize_text(skill) for skill in job.skills]
    experience = job.experience
    return ProcessedJob(
        job_id= job_id,
        skills=skills,
        experience=experience,
        responsibilities=[],
        education=[],
        keywords=[],
    )

