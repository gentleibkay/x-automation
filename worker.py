import time
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from storage import init_db, save_drafts
from generator import compose_drafts
from trends import get_trends


def wait_for_disk():
    """Wait until Render has mounted the shared disk at /app/data."""
    for _ in range(20):  # up to ~10 seconds
        if os.path.isdir("/app/data") and os.path.ismount("/app/data"):
            print("[worker] Shared disk is mounted at /app/data")
            return True
        print("[worker] Waiting for /app/data mount...")
        time.sleep(0.5)
    print("[worker] WARNING: Disk never mounted — using fallback ephemeral FS")
    return False


def job_generate():
    print("[worker] Running job_generate...")

    # Ensure disk is mounted before touching DB
    wait_for_disk()

    # Initialize DB ONLY after disk is mounted
    print("[worker] Initializing database in job...")
    init_db()

    # Load trends
    print("[worker] Fetching trends...")
    trends = get_trends()

    # Generate drafts
    print("[worker] Generating drafts...")
    drafts = compose_drafts(trends)

    # Save drafts into shared DB
    print("[worker] Saving drafts to DB...")
    save_drafts(drafts)

    print("[worker] Saved", len(drafts), "drafts")


def start_scheduler():
    scheduler = BlockingScheduler()

    # every minute for testing (later: cron hour=..., minute=...)
    scheduler.add_job(job_generate, "interval", minutes=1)

    print("[worker] Scheduler starting...")
    scheduler.start()


if __name__ == "__main__":
    print("[worker] Starting worker...")

    # DO NOT RUN init_db() HERE ANYMORE!
    # The disk may not be mounted yet during startup.
    # init_db()

    start_scheduler()
