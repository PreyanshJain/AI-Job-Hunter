from datetime import datetime
from pydantic import BaseModel, Field

class Experience(BaseModel):
    company: str = ""
    role: str = ""
    start_date: str = ""
    end_date: str = ""
    location: str = ""
    responsibilities: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)

class Project(BaseModel):
    project_name: str = ""
    project_description: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)

class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str = ""
    start_date: str = ""
    end_date: str = ""
    location: str = ""
    cgpa: str = ""

class SkillCategory(BaseModel):
    category: str = ""
    skills: list[str] = Field(default_factory=list)

class PersonalDetails(BaseModel):
    name: str
    email: str = ""
    phone_number: str = ""
    linkedin: str = ""
    github: str = ""

class ProcessedJob(BaseModel):
    job_id: str
    skills: list[str] 
    experience: str = ""
    responsibilities:list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)

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
    personal_details: PersonalDetails
    summary: str = ""
    education: list[Education] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    internships: list[Experience] = Field(default_factory=list)
    skills: list[SkillCategory] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)

class Application(BaseModel):
    job_id: str
    resume_version: str
    match_score: int
    ats_score: int
    status: str
    applied_at: datetime
    notes: str