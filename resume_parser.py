from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import pdfplumber

load_dotenv()

# Use Groq-compatible OpenAI client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# def extract_resume_data_with_gpt(resume_text):
    prompt = f"""
You are a helpful assistant. Extract structured data from the following resume text.

Return valid JSON with these fields:
- name
- summary
- skills (list of strings)
- education (list of dicts: degree, field, year)
- work_experience (list of dicts: role, company, duration)
- projects (list of dicts: title, description)
- certifications (list of strings)
- achievements (list of strings)

Resume Text:
\"\"\"{resume_text}\"\"\"
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",  # Groq's LLaMA3 model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    raw_output = response.choices[0].message.content
    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        print("⚠️ Invalid JSON returned:")
        print(raw_output)
        return None

def extract_resume_data_with_gpt(resume_text):
    prompt = f"""
You are a helpful assistant. Extract structured data from the following resume text.

Return only valid JSON with **any** of these fields (only include those present in the text):
- name
- summary
- skills (list of strings)
- education (list of dicts: degree, field, year)
- work_experience (list of dicts: role, company, duration)
- projects (list of dicts: title, description)
- certifications (list of strings)
- achievements (list of strings)

Resume Text:
\"\"\"{resume_text}\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # For Groq
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        raw_output = response.choices[0].message.content.strip()
        data = json.loads(raw_output)

        if not isinstance(data, dict) or not data:
            print("⚠️ GPT returned empty or malformed JSON.")
            return None

        return data

    except json.JSONDecodeError:
        print("⚠️ GPT returned invalid JSON:")
        print(raw_output)
        return None
    except Exception as e:
        print("❌ Error during GPT call:", e)
        return None
