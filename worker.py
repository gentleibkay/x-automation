import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

# Correct imports
from storage import save_drafts, init_db
from generator import compose_drafts
from trends import get_trends


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def job_generate():
    try:
        logger.info("Running job_generate...")

        trends = get_trends()
        drafts = compose_drafts(trends)

        save_drafts(drafts)
        logger.info(f"Saved {len(drafts)} drafts")

    except Exception as e:
        logger.error(f"Error in job_generate: {e}", exc_info=True)


def main():
    # Initialize DB before scheduling anything
    try:
        logger.info("Initializing database...")
        init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}", exc_info=True)

    scheduler = BlockingScheduler(timezone=os.getenv("TIMEZONE", "UTC"))

    # Run immediately on container start
    scheduler.add_job(job_generate, "date")

    # Regular schedule
    scheduler.add_job(job_generate, "cron", hour=9, minute=0)
    scheduler.add_job(job_generate, "cron", hour=13, minute=0)
    scheduler.add_job(job_generate, "cron", hour=17, minute=0)
    scheduler.add_job(job_generate, "cron", hour=21, minute=30)

    logger.info("Scheduler starting...")
    scheduler.start()


if __name__ == "__main__":
    main()
