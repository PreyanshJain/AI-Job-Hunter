from datetime import datetime
from pydantic import BaseModel

class Job(BaseModel):
    job_id: str
    title: str
    company: str
    location: str
    url: str
    description: str
    skills: list[str]
    experience: str
    source: str

class Resume(BaseModel):
    name: str
    summary: str
    education: list[str]
    experience: list[str]
    projects: list[str]
    skills: list[str]
    certifications: list[str]

class Application(BaseModel):
    job_id: str
    resume_version: str
    match_score: int
    ats_score: int
    status: str
    applied_at: datetime
    notes: str