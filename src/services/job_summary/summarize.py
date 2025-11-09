from core.llm import make_llm
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

SUMMARY_SYS = """
You are a professional job description summarizer. Your task is to analyze job descriptions and create clear, concise summaries.

For each job description, extract and summarize:
- Key responsibilities and duties
- Required qualifications and skills
- Preferred qualifications (if mentioned)
- Compensation and benefits (if mentioned)
- Important details like location, work arrangement (remote/hybrid/onsite), and employment type

Keep summaries factual, well-organized, and easy to scan. Use bullet points where appropriate.
Highlight any unique or standout aspects of the role.

Format your response in markdown with the following structure:
- Use ## subheadings for each of the five main categories above
- Under each subheading, provide 2-4 bullet points with specific details
- Ensure the markdown is clean and ready to be rendered in an email
"""


class SummaryAgent:
    def __init__(self):
        try:
            self.llm = make_llm()
        except Exception as e:
            print(f"SummaryAgent error: {e}")

    def summarize_job(self, job_description: str | None = None) -> AIMessage:
        prompt = [
            SystemMessage(content=SUMMARY_SYS),
            HumanMessage(content=job_description),
        ]
        summary = self.llm.invoke(prompt)
        return summary
