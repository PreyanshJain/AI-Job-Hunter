from pydantic import ValidationError
from app.models import Resume, MatchResult
from app.llm.llm_service import LLMService
from app.job_repository import JobRepository
from app.storage import save_json, load_json
from app.pdf_extractor import extract_text
from app.job_processor import process_job
from app.matching_engine import extract_resume_skills, match_skills, calculate_match_score
from app.resume_parser import (
    parse_resume,
    parse_education,
    parse_experience,
    parse_projects,
    parse_skills,
    combine_bullet_lines,
)


job_json_path = r"D:\Projects\AI-Job-Hunter\data\job.json"
resume_json_path = r"D:\Projects\AI-Job-Hunter\data\resume.json"
application_json_path = r"D:\Projects\AI-Job-Hunter\data\application.json"

resume_path = r"D:\Projects\AI-Job-Hunter\documents\Preyansh_Jain_AI_Engineer_Resume_2.pdf"
text, personal_details = extract_text(resume_path)
if not text:
    print("Resume extraction failed!")
    exit()
try:
    sections = parse_resume(text)
    sections["personal_details"] = personal_details
    sections["education"] = parse_education(sections["education"])
    sections["experience"] = parse_experience(sections["experience"])
    sections["projects"] = parse_projects(sections.get("projects", []))
    sections["skills"] = parse_skills(sections["skills"])
    sections["certifications"] = combine_bullet_lines(sections.get("certifications", []))
    sections["internships"] = parse_experience(sections.get("internships", []))
    sections["achievements"] = combine_bullet_lines(sections.get("achievements", []))
    resume = Resume.model_validate(sections)
    save_json(resume, resume_json_path)
    loaded_data = load_json(resume_json_path)
    loaded_resume = Resume.model_validate(loaded_data)
    resume_skills = extract_resume_skills(loaded_resume)

except ValidationError as error:
    print("Resume validation failed:")
    print(error)
    raise

repository = JobRepository(job_json_path)
jobs = repository.get_all()
# jobs = [all_jobs[0]]
match_results = []
model = "qwen3:4b"
llm_service = LLMService(model)
for job in jobs:
    processed_job = process_job(job)
    matched_skills, missing_skills, remaining_resume_skills = match_skills(resume_skills, processed_job.skills)
    print("Matched:", matched_skills)
    print("Missing:", missing_skills)
    print("Remaning:", remaining_resume_skills)
    if missing_skills and remaining_resume_skills:
        for missing_skill in missing_skills.copy():
            prompt = f"""
            You are a strict resume skill-matching system.
            Resume skills: {remaining_resume_skills}
            Job skill: {missing_skill}
            
            Determine whether at least one resume skill is genuinely
            equivalent to the job skill.
            
            Return true ONLY when:
            - Both terms refer to the same skill or technology.
            - One term is a recognized abbreviation or alternative name.
            - Differences are only formatting, capitalization,
              spacing, hyphens, or singular/plural forms.
            
            Return false when a skill is merely related to the job skill.
            
            Examples:
            - RAG and Retrieval-Augmented Generation: true
            - LLM and LLMs: true
            - Scikit-learn and scikit-learn: true
            - Python and Docker: false
            - Generative AI and OpenAI: false
            - Vector Search and Vector Database: false
            - Scikit-learn and Machine Learning: false
            
            If match is true:
            - Put the exact resume skill that caused the match
              in "resume_skill".
            
            If match is false:
            - Set "resume_skill" to null.
            
            Do not invent a resume skill.
            The value of "resume_skill" must come from the
            provided Resume skills list.
            
            Do not explain your answer.
            
            Return exactly this JSON structure:
            
            {{"match": true, "resume_skill": "exact resume skill"}}
            
            or
            
            {{"match": false, "resume_skill": null}}
            
            Examples:

            Equivalent skills → true:
            - Job: LLM
              Resume: LLMs
              Result: true
            
            - Job: Retrieval-Augmented Generation
              Resume: RAG
              Result: true
            
            - Job: Natural Language Processing
              Resume: NLP
              Result: true
            
            - Job: scikit-learn
              Resume: scikit-learn
              Result: true
            
            
            Related but NOT equivalent → false:
            - Job: OpenAI
              Resume: LLMs
              Result: false
            
            - Job: Vector Database
              Resume: Vector Search
              Result: false
            
            - Job: Machine Learning
              Resume: scikit-learn
              Result: false
            
            - Job: Docker
              Resume: Kubernetes
              Result: false
            
            - Job: FastAPI
              Resume: Python
              Result: false
            
            - Job: Azure
              Resume: AWS
              Result: false
            
            - Job: LangChain
              Resume: RAG
              Result: false
            - Job: Vector Database
              Resume: Vector Search
              Result: false
            
            - Job: Vector Search
              Resume: Vector Database
              Result: false
            """
            response = llm_service.generate(prompt)
            if response["match"] and response["resume_skill"] in remaining_resume_skills:
                matched_skills.append(missing_skill)
                missing_skills.remove(missing_skill)


            elif not response["match"]:
                response["resume_skill"] = None

    print("Updated Matched:",matched_skills)
    print("Updated Missing:",missing_skills)
    score = calculate_match_score(matched_skills, processed_job.skills)
    match_results.append(MatchResult(
        job_id=processed_job.job_id,
        match_score=score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
    )
    )
    print("_______________________________________________")
