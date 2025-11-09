"""
Web scraping job search implementation
No authentication required - scrapes public job boards
"""

import requests

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("BeautifulSoup not installed. Install with: pip install beautifulsoup4")
    BeautifulSoup = None

from typing import List, Dict, Optional
from urllib.parse import urljoin, quote
from core.db_models import JobPosting
import time


class PublicJobScraper:
    """
    Scrapes job postings from public job boards that don't require login
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )

    def search_indeed_jobs(
        self, query: str, location: str = "United States", max_results: int = 10
    ) -> List[JobPosting]:
        """
        Search Indeed for jobs (public, no auth required)
        """
        jobs = []
        try:
            # Indeed search URL
            base_url = "https://www.indeed.com/jobs"
            params = {
                "q": query,
                "l": location,
                "limit": min(max_results, 50),  # Indeed's limit
            }

            response = self.session.get(base_url, params=params)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Find job cards (Indeed's structure as of 2024)
            job_cards = soup.find_all(
                "div", {"class": lambda x: x and "job_seen_beacon" in x}
            )

            for card in job_cards[:max_results]:
                try:
                    # Extract job details
                    title_elem = card.find("a", {"data-jk": True})
                    title = title_elem.get_text(strip=True) if title_elem else "N/A"

                    company_elem = card.find(
                        "span", {"class": lambda x: x and "companyName" in x}
                    )
                    company = (
                        company_elem.get_text(strip=True) if company_elem else "N/A"
                    )

                    location_elem = card.find(
                        "div", {"class": lambda x: x and "companyLocation" in x}
                    )
                    job_location = (
                        location_elem.get_text(strip=True) if location_elem else "N/A"
                    )

                    # Job URL
                    job_url = (
                        urljoin("https://www.indeed.com", title_elem["href"])
                        if title_elem and title_elem.get("href")
                        else ""
                    )

                    # Summary/snippet
                    summary_elem = card.find(
                        "div", {"class": lambda x: x and "summary" in x}
                    )
                    description = (
                        summary_elem.get_text(strip=True) if summary_elem else "N/A"
                    )

                    job = JobPosting(
                        title=title,
                        company=company,
                        location=job_location,
                        description=description,
                        url=job_url,
                        source="Indeed (Public Scraping)",
                    )
                    jobs.append(job)

                except Exception as e:
                    print(f"Error parsing job card: {e}")
                    continue

            # Be respectful - add delay
            time.sleep(1)

        except requests.RequestException as e:
            print(f"Error scraping Indeed: {e}")

        return jobs

    def search_remote_ok_jobs(
        self, query: str, max_results: int = 10
    ) -> List[JobPosting]:
        """
        Search Remote OK for remote jobs (public API, no auth required)
        """
        jobs = []
        try:
            # Remote OK has a simple API
            api_url = "https://remoteok.io/api"
            response = self.session.get(api_url)
            response.raise_for_status()

            data = response.json()

            # Filter jobs by query
            query_lower = query.lower()
            count = 0

            for job_data in data[1:]:  # First item is metadata
                if count >= max_results:
                    break

                # Check if query matches title or tags
                title = job_data.get("position", "").lower()
                tags = " ".join(job_data.get("tags", [])).lower()

                if query_lower in title or any(
                    term in tags for term in query_lower.split()
                ):
                    job = JobPosting(
                        title=job_data.get("position", "N/A"),
                        company=job_data.get("company", "N/A"),
                        location="Remote",
                        description=job_data.get("description", "N/A"),
                        url=job_data.get("url", ""),
                        salary_range=job_data.get("salary_range", None),
                        source="Remote OK",
                    )
                    jobs.append(job)
                    count += 1

        except requests.RequestException as e:
            print(f"Error fetching from Remote OK: {e}")

        return jobs


def search_ai_engineer_jobs_no_auth(
    location: str = "United States",
) -> List[JobPosting]:
    """
    Search for AI Engineer jobs using non-authenticated sources
    """
    scraper = PublicJobScraper()

    all_jobs = []

    # Search Indeed
    indeed_jobs = scraper.search_indeed_jobs("AI Engineer", location, 5)
    all_jobs.extend(indeed_jobs)

    # Search Remote OK
    remote_jobs = scraper.search_remote_ok_jobs("AI Engineer", 5)
    all_jobs.extend(remote_jobs)

    return all_jobs
