import pytest
from app.resume_parser import parse_resume, parse_experience
from app.models import Resume


def test_parse_resume_sections():
    text = """
    Summary
    Python developer with AI experience.

    Experience
    Python Developer
    September 2024 — Present
    Infosys
    Pune

    Education
    B.E., Institute of Engineering and Technology
    2017 — 2021

    Skills
    Programming
    Python, SQL

    Projects
    AI Resume Optimizer | Python, LLM, NLP
    """

    result = parse_resume(text)

    assert "summary" in result
    assert "experience" in result
    assert "education" in result
    assert "skills" in result
    assert "projects" in result


def test_parse_experience():
    lines = [
        "Python Developer",
        "September 2024 — Present",
        "Infosys",
        "Pune",
        "• Built Python automation tools.",
        "• Worked with NLP.",
    ]

    result = parse_experience(lines)

    assert len(result) == 1
    assert result[0]["role"] == "Python Developer"
    assert result[0]["company"] == "Infosys"
    assert result[0]["location"] == "Pune"
    assert result[0]["start_date"] == "September 2024"
    assert result[0]["end_date"] == "Present"
    assert len(result[0]["responsibilities"]) == 2


def test_resume_validation():
    resume_data = {
        "personal_details": {
            "name": "Test User",
            "email": "test@example.com",
            "phone_number": "1234567890",
            "linkedin": "",
            "github": ""
        },
        "summary": "Python developer",
        "education": [],
        "experience": [],
        "projects": [],
        "internships": [],
        "skills": [],
        "certifications": [],
        "achievements": []
    }

    resume = Resume.model_validate(resume_data)

    assert isinstance(resume, Resume)