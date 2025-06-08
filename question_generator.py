# question_generator.py

from openai import OpenAI  # or from openai import OpenAI if you're using OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Use Groq-compatible OpenAI client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)  # or OpenAI(...)

def generate_questions(resume_data, model="llama3-70b-8192", num_questions=10):
    prompt = f"""
        You are an expert technical interviewer.

        Your task is to generate {num_questions} interview questions for a candidate based on their resume. Please follow these instructions carefully:

        1. Start with **basic questions** to ease the candidate into the interview.
        2. **Do not immediately ask advanced or in-depth questions** about projects or experiences.
        3. Ask **project-specific questions later**, and only after referencing some related basic concepts.
        4. If a skill or technology appears only in a project or once in the resume, assume the candidate may be **familiar but not deeply experienced**. Ask beginner-level or exploratory questions in that case.
        5. If a skill is listed under 'skills' and used in multiple projects, you can assume a higher level of confidence and ask deeper questions.
        6. Use a mix of:
        - Skill-based questions
        - Project-related questions (after warmup)
        - Education or theoretical questions
        - Behavioral/teamwork/communication questions

        7. For tricky or open-ended questions, include a short explanation to help the candidate understand what you're asking.

        Resume Data (in JSON format):
        {resume_data}
    """

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    questions=response.choices[0].message.content.strip()

    return questions
