from core.llm import make_llm
from core.models import ApplicationMaterials
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from typing import Dict

APP_SYS = f"""
You are an expert career coach with a special focus on application materials. you are highly skilled in combining a job description & an applicant's personal information to write concise, impactful application materials. NEVER misrepresent the applicant's experience or skillset. frame skills & experiences in a way that specifically addresses the job description
"""
COVER_LETTER_INSTRUCTIONS = """
Cover Letter Guidelines:
• Length: Aim for 3/4 of a page, typically around 300-500 words.
• Structure:
  - Opening: Start with a strong introduction that captures attention.
  - Body: Highlight relevant experiences, skills, and achievements that align with the job description.
  - Closing: End with a compelling conclusion that reiterates your interest and fit for the role.
• Tone: Maintain a professional yet personable tone. Show enthusiasm for the role and company.
• Customization: Tailor the content to address the specific job requirements and company culture.
• Proofreading: Ensure the letter is free from grammatical errors and typos.
"""
RESUME_INSTRUCTIONS = """
Resume Guidelines:
• Length: Keep it concise, ideally 1-2 pages.
• Format: Use a clean, professional layout with clear headings and bullet points.
• Content:
  - Contact Information: Include your name, phone number, email, and LinkedIn profile.
  - Summary: A brief statement highlighting your career goals and key qualifications.
  - Experience: List relevant work experiences in reverse chronological order, focusing on achievements and responsibilities that match the job description.
  - Skills: Highlight technical and soft skills pertinent to the role.
  - Education: Include degrees, certifications, and relevant coursework.
• Customization: Tailor your resume to emphasize experiences and skills that align with the job description.
• Proofreading: Ensure the resume is free from grammatical errors and typos.
"""


class AppAgent:
    def __init__(self):
        try:
            self.llm = make_llm()
        except Exception as e:
            print(f"AppAgent error: {e}")

    def write_cover_letter(
        self, job_description: str | None = None, applicant_info: str | None = None
    ) -> AIMessage:
        msg = f"""
use {COVER_LETTER_INSTRUCTIONS} to write a cover letter for the following job & applicant info:            
JOB DESCRIPTION:
{job_description}

APPLICANT_INFO:
{applicant_info}
"""
        prompt = [
            SystemMessage(content=APP_SYS),
            HumanMessage(content=msg),
        ]
        cover_letter = self.llm.invoke(input=prompt)

        return cover_letter  # type: ignore[return-value]

    def write_resume(
        self, job_description: str | None = None, applicant_info: str | None = None
    ) -> AIMessage:
        msg = f"""
use {RESUME_INSTRUCTIONS} to write a resume for the following job & applicant info:
JOB DESCRIPTION:
{job_description}


APPLICANT_INFO:
{applicant_info}
"""
        prompt = [SystemMessage(content=APP_SYS), HumanMessage(content=msg)]
        resume = self.llm.invoke(input=prompt)
        return resume  # type: ignore[return-value]


def create_job_app(
    job_description: str, applicant_info: str = ""
) -> ApplicationMaterials:
    app_agent = AppAgent()
    resume_content = app_agent.write_resume(
        job_description=job_description, applicant_info=applicant_info
    ).content
    cover_letter_content = app_agent.write_cover_letter(
        job_description=job_description, applicant_info=applicant_info
    ).content

    resume = (
        str(resume_content) if not isinstance(resume_content, str) else resume_content
    )
    cover_letter = (
        str(cover_letter_content)
        if not isinstance(cover_letter_content, str)
        else cover_letter_content
    )

    return ApplicationMaterials(resume=resume, cover_letter=cover_letter)
