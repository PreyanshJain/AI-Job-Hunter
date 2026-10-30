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
            You are a conservative resume skill-equivalence classifier.

            Your task is to determine whether any skill in the resume list
            is IDENTICAL IN MEANING to the job skill.

            Resume skills: {remaining_resume_skills}
            Job skill: {missing_skill}

            DECISION RULES:

            1. Return true only if a resume skill and the job skill refer
               to the same skill, technology, or capability.

            2. Accept recognized abbreviations, alternative names, and
               harmless formatting differences.

            3. Do NOT match skills just because they are related, commonly
               used together, belong to the same field, or have overlapping
               functionality.

            4. A tool/library is not equivalent to the field it supports.
               A platform/company is not equivalent to a technology category.
               A database is not equivalent to the search operation it supports.

            5. When uncertain, return false. Do not guess or infer equivalence.

            IMPORTANT EXAMPLES:

            Job: Retrieval-Augmented Generation
            Resume: RAG
            Decision: true

            Job: Natural Language Processing
            Resume: NLP
            Decision: true

            Job: LLM
            Resume: LLMs
            Decision: true

            Job: Vector Database
            Resume: Vector Search
            Decision: false

            Job: Vector Search
            Resume: Vector Database
            Decision: false

            Job: Machine Learning
            Resume: scikit-learn
            Decision: false

            Job: Generative AI
            Resume: OpenAI
            Decision: false

            Job: Docker
            Resume: Kubernetes
            Decision: false

            Job: FastAPI
            Resume: Python
            Decision: false

            Job: Azure
            Resume: AWS
            Decision: false

            Job: LangChain
            Resume: RAG
            Decision: false
            
            Job: scikit-learn
            Resume: scikit‑learn
            Decision: true

            OUTPUT RULES:

            - If true, resume_skill must contain the exact matching skill
              copied from the provided resume skills list.
            - If false, resume_skill must be null.
            - Never invent or modify a resume skill.
            - Return valid JSON only. Do not include explanations or Markdown.

            Return exactly one of these structures:

            {{"match": true, "resume_skill": "exact resume skill"}}

            {{"match": false, "resume_skill": null}}
            """
            response = llm_service.generate(prompt)
            if (
                    response["match"] is True
                    and isinstance(response["resume_skill"], str)
                    and response["resume_skill"] in remaining_resume_skills
                    and missing_skill not in matched_skills
            ):
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
