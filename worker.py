import os
import time
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from storage import compose_drafts, save_drafts, init_db
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
    # 🔥 Ensure database is created in WORKER too (fixes your error)
    try:
        logger.info("Initializing database...")
        init_db()
        logger.info("DB initialized successfully")
    except Exception as e:
        logger.error(f"DB init failed: {e}", exc_info=True)

    scheduler = BlockingScheduler(timezone=os.getenv("TIMEZONE", "UTC"))

    # First run immediately
    scheduler.add_job(job_generate, "date", run_date=None)

    # Scheduled runs
    scheduler.add_job(job_generate, "cron", hour=9, minute=0)
    scheduler.add_job(job_generate, "cron", hour=13, minute=0)
    scheduler.add_job(job_generate, "cron", hour=17, minute=0)
    scheduler.add_job(job_generate, "cron", hour=21, minute=30)

    logger.info("Scheduler starting...")
    scheduler.start()


if __name__ == "__main__":
    main()
