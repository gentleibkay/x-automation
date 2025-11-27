import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from trends import fetch_trends
from generator import compose_drafts
from storage import save_drafts
from notifier import notify_new_drafts

logging.basicConfig(level=logging.INFO)
TZ = os.getenv("TIMEZONE", "Africa/Lagos")

sched = BlockingScheduler(timezone=TZ)

def job_generate():
    try:
        logging.info("Running job_generate...")
        trends = fetch_trends()
        drafts = compose_drafts(trends)
        if drafts:
            save_drafts(drafts)
            notify_new_drafts(drafts)
            logging.info(f"Saved {len(drafts)} drafts")
        else:
            logging.info("No drafts generated")
    except Exception as e:
        logging.exception("Error in job_generate: %s", e)

sched.add_job(job_generate, 'cron', hour='9', minute='0')
sched.add_job(job_generate, 'cron', hour='13', minute='0')
sched.add_job(job_generate, 'cron', hour='17', minute='0')
sched.add_job(job_generate, 'cron', hour='21', minute='30')

if __name__ == "__main__":
    logging.info("Scheduler starting...")
    job_generate()  # run immediately once
    sched.start()

