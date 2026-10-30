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
        skills= ["Python", "Java", "JavaScript", "C++", "scikit‑learn"],
        experience= "3 years",
        source="Naukri"
    )
    processed_job = process_job(job)
    assert processed_job.skills == [
        "python",
        "java",
        "javascript",
        "c++",
        "scikit-learn"
    ]
    assert job.experience == processed_job.experience
    assert job.job_id == processed_job.job_id
    assert processed_job.skills[-1] == "scikit-learn"


def test_normalize_text_handles_unicode_hyphen():
    unicode_hyphen = normalize_text("scikit‑learn")
    regular_hyphen = normalize_text("scikit-learn")

    assert unicode_hyphen == regular_hyphen