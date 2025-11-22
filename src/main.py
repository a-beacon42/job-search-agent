import logging
from services.job_discovery.discover import find_ai_engineer_jobs
from services.job_summary.summarize import SummaryAgent
from core.db import get_session
from core.repositories import JobSearchQueryRepo, JobPostingRepo, JobSummaryRepo

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("job_search_agent.log")],
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting job search process...")
    """
    -- interview coach should be separate app with access to db --
        * could this be a tab in the streamlit UI that opens an interactive chat window? 
        * using a speech model for interview practice
    """
    logger.info("Establishing database connection...")
    try:
        db_session = get_session()
        logger.info(f"Database connection successful: {db_session}")
        job_posting_repo = JobPostingRepo(db_session)
        job_summary_repo = JobSummaryRepo(db_session)
    except Exception as e:
        logger.error(f"Database connection failed: {e}")

    # 1. find jobs - service
    try:  # find new ai engineer jobs
        logger.info("🔍 Searching for AI Engineer jobs...")
        logger.info("=" * 80)
        jobs = find_ai_engineer_jobs()

        logger.info("=" * 80)
        logger.info(f"Found {len(jobs)} AI Engineer jobs")

        for i, job in enumerate(jobs, 1):
            logger.info(f"{i}. {job.title}")
            logger.info(f"   Company: {job.company}")
            logger.info(f"   Location: {job.location}")
            logger.info(f"   Source: {job.source}")
            if job.url:
                logger.info(f"   URL: {job.url}")
            logger.info(f"   Description: {job.description[:200]}...")
            logger.info("-" * 50)
    except Exception as e:
        logger.error(f"Job search failed: {e}")

    try:  # add jobs to db
        logger.info("=" * 80)
        for job in jobs:
            logger.info(f"Writing job '{job.title}' to database...")
            job_posting_repo.add(job)
        logger.info(f"Successfully wrote {len(jobs)} jobs to database")
    except Exception as e:
        logger.error(f"Database write failed: {e}")

    # 2. summarize - graph
    try:  # summarize job posts
        summarizer = SummaryAgent()
        # get new jobs from db that haven't been summarized yet
        new_jobs = job_posting_repo.get_new()
        for job in new_jobs:
            if not job.id:
                logger.warning(f"Skipping job without ID: {job.title}")
                continue
            summary = summarizer.summarize_job(job.description)
            summary.job_posting_id = job.id
            logger.info(
                f"Generated summary for job: {job.title} ({summary.job_posting_id})"
            )
            logger.debug(f"Summary content: {summary}")
            logger.info("*-^-" * 20)
            job_posting_repo.update_job(job_id=job.id, job_summary_id=summary.id)
            job_summary_repo.add(summary)

    except Exception as e:
        logger.error(f"Job summarization failed: {e}")

    # 3. send notification - service
    try:  # send email
        """
        MVP = display summaries & URL to job post
        improved = display form with select 0-many & submit form with 'selected_jobs' -> triggers app to generate job app materials, send email notification
        """
        pass
    except Exception as e:
        logger.error(f"Notification error: {e}")

    # 4. listen for selection
    # 5. write application materials - agent
    # 6. send notification


if __name__ == "__main__":
    main()
