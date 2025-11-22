from src.core.llm import make_llm
from langchain_core.messages import SystemMessage, HumanMessage
from src.core.models import JobSummary

SUMMARY_SYS = """
You are a professional job description summarizer. Your task is to analyze job descriptions and create clear, **concise** summaries.
Keep summaries factual, well-organized, and **easy to scan**. Use a maximum of 3 bullet points per section and a maximum of 25 words per bullet, use ';' instead of 'and ', there's no need to continually repeat the same word to describe the job, i.e. if the role is on the security team, use the word 'security' sparingly. put the exact, case-sensitive string: 'not listed' in places where the information is not available in the job description
"""


class SummaryAgent:
    def __init__(self):
        try:
            self.llm = make_llm()
        except Exception as e:
            print(f"SummaryAgent error: {e}")

    def summarize_job(self, job_description: str | None = None) -> JobSummary:
        prompt = [
            SystemMessage(content=SUMMARY_SYS),
            HumanMessage(content=job_description),
        ]
        summary = self.llm.with_structured_output(JobSummary).invoke(input=prompt)

        return summary  # type: ignore[return-value]
