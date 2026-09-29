from pypdf import PdfReader

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_text_from_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text = text + page_text

    return text


def extract_skills(text):

    skills_list = [
        'Python',
        'Django',
        'Flask',
        'HTML',
        'CSS',
        'JavaScript',
        'SQL',
        'MySQL',
        'REST API',
        'Git',
        'GitHub',
        'Machine Learning',
        'Artificial Intelligence'
    ]

    found_skills = []

    text = text.lower()

    for skill in skills_list:

        if skill.lower() in text:

            found_skills.append(skill)

    return found_skills


def match_skills(candidate_skills, job_skills):

    candidate_skills = candidate_skills.split(',')
    job_skills = job_skills.split(',')

    matched_skills = []
    missing_skills = []

    candidate_skill_list = []

    for skill in candidate_skills:

        candidate_skill_list.append(
            skill.strip().lower()
        )

    for skill in job_skills:

        skill = skill.strip()

        if skill.lower() in candidate_skill_list:

            matched_skills.append(skill)

        else:

            missing_skills.append(skill)

    if len(job_skills) > 0:

        match_percentage = (
            len(matched_skills) / len(job_skills)
        ) * 100

    else:

        match_percentage = 0

    recommendation = ""

    if len(missing_skills) > 0:

        recommendation = (
            "You should improve your skills in: "
            + ", ".join(missing_skills)
        )

    else:

        recommendation = (
            "Your skills match all the required skills."
        )

    return (
        matched_skills,
        missing_skills,
        match_percentage,
        recommendation
    )


def calculate_ai_match(resume_text, job_text):

    if not resume_text or not job_text:

        return 0

    # --------------------------------
    # PART 1: Full text similarity
    # --------------------------------

    text_documents = [
        resume_text,
        job_text
    ]

    text_vectorizer = TfidfVectorizer(
        stop_words='english'
    )

    text_vectors = text_vectorizer.fit_transform(
        text_documents
    )

    text_similarity = cosine_similarity(
        text_vectors[0:1],
        text_vectors[1:2]
    )

    text_score = (
        text_similarity[0][0] * 100
    )


    # --------------------------------
    # PART 2: Skill similarity
    # --------------------------------

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_text
    )

    skill_score = 0

    if resume_skills and job_skills:

        resume_skill_text = " ".join(
            resume_skills
        )

        job_skill_text = " ".join(
            job_skills
        )

        skill_documents = [
            resume_skill_text,
            job_skill_text
        ]

        skill_vectorizer = TfidfVectorizer()

        skill_vectors = skill_vectorizer.fit_transform(
            skill_documents
        )

        skill_similarity = cosine_similarity(
            skill_vectors[0:1],
            skill_vectors[1:2]
        )

        skill_score = (
            skill_similarity[0][0] * 100
        )


    # --------------------------------
    # PART 3: Combined AI/NLP score
    # --------------------------------

    ai_match_percentage = (
        (text_score * 0.40)
        + (skill_score * 0.60)
    )

    return round(
        ai_match_percentage,
        2
    )