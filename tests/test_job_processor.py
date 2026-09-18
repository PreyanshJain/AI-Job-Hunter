from app.models import Job
from app.job_processor import process_job, normalize_text


def test_process_job_normalizes_all_skills():
    job = Job(
        job_id= "job_001",
        title= "Software Developer",
        company= "Cbre",
        location="Bangalore",
        url="https://www.cbre.com",
        description= "We are seeking a Software Developer to design, build, and maintain efficient software applications.",
        skills= ["Python", "Java", "JavaScript", "C++"],
        experience= "3 years",
        source="Naukri"
    )
    skills = [normalize_text(skill) for skill in job.skills]
    processed_job = process_job(job)
    assert processed_job.skills == [
        "python",
        "java",
        "javascript",
        "c++"
    ]
    assert job.experience == processed_job.experience
    assert job.job_id == processed_job.job_id