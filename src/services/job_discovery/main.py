"""
Main job discovery service coordinator
Manages multiple job sources without authentication dependencies
"""

from typing import List
from src.core.models import JobPosting, JobSearchQuery


class JobDiscoveryService:
    """
    Coordinates multiple job search sources that don't require authentication
    """

    def __init__(self):
        self.sources = []  # Tuple(str, SearchObject)
        self._initialize_sources()

    def _initialize_sources(self):
        """Initialize available job sources"""
        try:
            from .sources.public_scraper import PublicJobScraper

            self.sources.append(("public_scraper", PublicJobScraper()))
        except ImportError:
            print("Public scraper not available (missing beautifulsoup4)")

        try:
            from .sources.serp_api import SerpAPIJobSearch
            import os

            if os.getenv("SERP_API_KEY"):
                self.sources.append(("serp_api", SerpAPIJobSearch()))
            else:
                print(
                    "SerpAPI not available (missing SERP_API_KEY environment variable)"
                )
        except ImportError:
            print("SerpAPI not available")

    def search_jobs(self, query: JobSearchQuery) -> List[JobPosting]:
        """
        Search for jobs across all available sources
        """
        all_jobs = []

        # todo - refactor sources to all expose .search_jobs() -> simplify this loop
        for source_name, source in self.sources:
            try:
                print(f"Searching {source_name} for '{query.keywords}'...")

                if source_name == "public_scraper":
                    # Public scraper methods
                    indeed_jobs = source.search_indeed_jobs(
                        query.keywords, query.location, query.max_results // 2
                    )
                    all_jobs.extend(indeed_jobs)

                    remote_jobs = source.search_remote_ok_jobs(
                        query.keywords, query.max_results // 2
                    )
                    all_jobs.extend(remote_jobs)

                elif source_name == "serp_api":
                    # SerpAPI method
                    serp_jobs = source.search_jobs(
                        query.keywords, query.location, query.max_results
                    )
                    all_jobs.extend(serp_jobs)

            except Exception as e:
                print(f"Error searching {source_name}: {e}")
                continue

        # Remove duplicates based on title + company
        seen = set()
        unique_jobs = []
        for job in all_jobs:
            key = (job.title.lower(), job.company.lower())
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)

        return unique_jobs[: query.max_results]

    def search_ai_engineer_jobs(
        self, location: str = "United States"
    ) -> List[JobPosting]:
        """
        Convenience method to search for AI Engineer jobs
        """
        query = JobSearchQuery(
            keywords="AI Engineer", location=location, max_results=20
        )
        return self.search_jobs(query)


# Convenience function for direct use
def find_ai_engineer_jobs(location: str = "United States") -> List[JobPosting]:
    """
    Find AI Engineer jobs without any authentication requirements
    """
    service = JobDiscoveryService()
    return service.search_ai_engineer_jobs(location)


def find_jobs(query_params: JobSearchQuery) -> List[JobPosting]:
    service = JobDiscoveryService()
    return service.search_jobs(query_params)
