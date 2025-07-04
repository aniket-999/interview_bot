from resume_parser import extract_text_from_pdf, extract_resume_data
from question_generator import generate_base_question, generate_followup_question
from interaction_engine import run_interaction

pdf_path = "resume.pdf"

# Step 1: Extract resume data
resume_text = extract_text_from_pdf(pdf_path)
resume_data = extract_resume_data(resume_text)

# Step 2: Begin dynamic questioning
question = generate_base_question(resume_data)

while question:
    followup = run_interaction(question, resume_data, generate_followup_question)
    question = followup  # if None, we move to next base question or end
