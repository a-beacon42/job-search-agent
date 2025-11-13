from src.services.job_discovery.discover import find_ai_engineer_jobs
from services.job_summary.summarize import SummaryAgent
from core.db import get_session
from core.repositories import JobSearchQueryRepo, JobPostingRepo


def main():
    print("Hello from job-search-agent!\n\nkicking off a search...\n")
    """
    
    -- interview coach should be separate app with access to db --
        * could this be a tab in the streamlit UI that opens an interactive chat window? 
        * using a speech model for interview practice
    """
    print("starting DB session...")
    try:
        db_session = get_session()
        print(f"SUCCESS! connected to {db_session.__dir__}")
        job_posting_repo = JobPostingRepo(db_session)
    except Exception as e:
        print(f"Error: {e}")

    # 1. find jobs - service
    # try:  # find new ai engineer jobs
    #     print("🔍 Searching for AI Engineer jobs...")
    #     print("=" * 60)
    #     jobs = find_ai_engineer_jobs()

    #     print(f"Found {len(jobs)} AI Engineer jobs:\n")

    #     for i, job in enumerate(jobs, 1):
    #         print(f"{i}. {job.title}")
    #         print(f"   Company: {job.company}")
    #         print(f"   Location: {job.location}")
    #         print(f"   Source: {job.source}")
    #         if job.url:
    #             print(f"   URL: {job.url}")
    #         print(f"   Description: {job.description[:200]}...")
    #         print("-" * 50)
    # except Exception as e:
    #     print(f"Error: {e}")

    # try:  # add jobs to db
    #     for job in jobs:
    #         print(f"\nwriting job: {job.title} to db...")
    #         job_posting_repo.add(job)
    #     print(f"wrote {len(jobs)} jobs to DB\n")
    # except Exception as e:
    #     print(f"Error: {e}")

    # 2. summarize - graph
    try:  # summarize job descriptions
        summarizer = SummaryAgent()
        # get jobs from db -- need id created in last step
        new_jobs = job_posting_repo.get_new()
        for job in new_jobs:
            if not job.id:
                print(f"skipping job without ID: {job.title}")
                continue
            summary = summarizer.summarize_job(job.description)
            print(f"\tjob summary:\n{summary}\n")
            print("*-^-" * 20)
            job_posting_repo.update_job(job_id=job.id, summary=summary.content)

    except Exception as e:
        print(f"Summarize Jobs Error: {e}")

    # 3. send notification - service
    try:  # send email
        """
        MVP = display summaries & URL to job post
        improved = display form with select 0-many & submit form with 'selected_jobs' -> triggers app to generate job app materials, send email notification
        """
        pass
    except Exception as e:
        print(f"...error: {e}")

    # 4. listen for selection
    # 5. write application materials - agent
    # 6. send notification


if __name__ == "__main__":
    main()
