"""
SerpAPI-based job search implementation
No authentication cookies required - just API key
"""

import os
from dotenv import load_dotenv
import requests
from typing import List, Dict, Optional
from core.db_models import JobPosting

load_dotenv()


class SerpAPIJobSearch:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("SERP_API_KEY")
        self.base_url = "https://serpapi.com/search"

    def search_jobs(
        self, query: str, location: str = "United States", num_results: int = 10
    ) -> List[JobPosting]:
        """
        Search for jobs using SerpAPI (Google Jobs)
        No authentication required beyond API key
        """
        if not self.api_key:
            raise ValueError(
                "SERP_API_KEY environment variable or api_key parameter required"
            )

        params = {
            "engine": "google_jobs",
            "q": query,
            "location": location,
            "api_key": self.api_key,
            "num": num_results,
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            jobs = []
            for job_data in data.get("jobs_results", []):
                job = JobPosting(
                    title=job_data.get("title", ""),
                    company=job_data.get("company_name", ""),
                    location=job_data.get("location", ""),
                    description=job_data.get("description", ""),
                    url=job_data.get("share_link", ""),
                    posted_date=job_data.get("detected_extensions", {}).get(
                        "posted_at", ""
                    ),
                    source="Google Jobs (SerpAPI)",
                )
                jobs.append(job)

            return jobs

        except requests.RequestException as e:
            print(f"Error searching jobs via SerpAPI: {e}")
            return []


def search_ai_engineer_jobs(location: str = "United States") -> List[JobPosting]:
    """
    Convenience function to search for AI Engineer jobs
    """
    searcher = SerpAPIJobSearch()
    return searcher.search_jobs("AI Engineer", location)
