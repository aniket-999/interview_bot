from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(openai_api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1", model="llama3-70b-8192")

def generate_base_question(resume_data):
    prompt_template = ChatPromptTemplate.from_template("""
        You are an expert technical interviewer. Based on this resume:
        {resume}
        
        Ask one base technical or behavioral interview question. 
        Do not ask follow-ups now.
    """)
    chain = prompt_template | llm
    return chain.invoke({"resume": resume_data["raw_text"]}).content

def generate_followup_question(previous_question, user_answer):
    prompt_template = ChatPromptTemplate.from_template("""
        Given the previous question:
        "{question}"

        And the candidate's answer:
        "{answer}"

        Analyze the response. If it's good, say "✅ Good answer. Moving on."
        Else, generate a follow-up question to dig deeper.
    """)
    chain = prompt_template | llm
    return chain.invoke({"question": previous_question, "answer": user_answer}).content
