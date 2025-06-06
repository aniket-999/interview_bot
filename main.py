from resume_parser import extract_text_from_pdf, extract_resume_data_with_gpt

pdf_path = "/mnt/d/interview_bot/interview_bot/resume.pdf"

print("🔍 Extracting text from resume...")
resume_text = extract_text_from_pdf(pdf_path)

print("🤖 Sending resume to GPT for parsing...")
resume_data = extract_resume_data_with_gpt(resume_text)

if resume_data:
    print("\n✅ Extracted Resume Data:")
    for key, value in resume_data.items():
        print(f"{key}:\n{value}\n")
else:
    print("❌ Could not extract useful data.")
