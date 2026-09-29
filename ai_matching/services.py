from openai import OpenAI


def generate_interview_questions(job_title, required_skills):

    client = OpenAI()

    prompt = f"""
Generate 5 interview questions for a fresher applying for this job.

Job Title:
{job_title}

Required Skills:
{required_skills}

The questions should test the candidate's knowledge of the required skills.

Return only the questions as a numbered list.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    return response.output_text