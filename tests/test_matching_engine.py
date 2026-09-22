from app.models import Resume, PersonalDetails, SkillCategory
from app.matching_engine import extract_resume_skills, match_skills, calculate_match_score

def test_extract_resume_skills():
    resume = Resume(
        personal_details = PersonalDetails(name='Preyansh Jain', email='preyansh749@gmail.com', phone_number='+91 9166100808', linkedin='https://www.linkedin.com/in/preyansh-jain-130550168/', github=''),
        summary = " ",
        education = [],
        experience = [],
        projects = [],
        internships = [],
        skills = [SkillCategory(category='Programming', skills=['Python', 'SQL']), SkillCategory(category='AI & ML', skills=['Generative AI', 'NLP', 'LLMs', 'Prompt Engineering', 'Text Classification', 'Sentiment Analysis',]), SkillCategory(category='AI Frameworks & Libraries', skills=['LangChain', 'Hugging Face', 'Scikit‑learn', 'NLTK', 'spaCy', 'NumPy', 'Pandas']), SkillCategory(category='LLM Concepts', skills=['Embeddings', 'Vector Search', 'RAG', 'Context Retrieval', 'Prompt Design']), SkillCategory(category='Databases & Tools', skills=['MySQL', 'Oracle SQL', 'Git', 'GitHub', 'Jupyter Notebook', 'VS Code'])],
        certifications = [],
        achievements = [],
    )
    resume_skills = extract_resume_skills(resume)

    assert resume_skills == ['python', 'sql', 'generative ai', 'nlp', 'llms', 'prompt engineering', 'text classification', 'sentiment analysis', 'langchain', 'hugging face', 'scikit‑learn', 'nltk', 'spacy', 'numpy', 'pandas', 'embeddings', 'vector search', 'rag', 'context retrieval', 'prompt design', 'mysql', 'oracle sql', 'git', 'github', 'jupyter notebook', 'vs code']



def test_match_skills():
    resume_skills = ["python", "rag", "docker"]
    job_skills = ["python", "langchain", "rag", "fastapi"]

    matched_skills, missing_skills = match_skills(resume_skills, job_skills)

    assert matched_skills == ["python", "rag"]
    assert missing_skills == ["langchain", "fastapi"]

def test_calculate_match_score():
    matched_skills = ["python", "rag"]
    job_skills = ["python", "langchain", "rag", "fastapi"]

    score = calculate_match_score(matched_skills, job_skills)
    assert score == 50.00

def test_calculate_match_score_with_no_job_skills():
    matched_skills = ["python", "rag"]
    job_skills = []

    score = calculate_match_score(matched_skills, job_skills)
    assert score == 0