import os
import time
from apscheduler.schedulers.blocking import BlockingScheduler

from trends import get_trends
from generator import compose_drafts
from storage import init_db, save_drafts


def wait_for_disk():
    """Wait for shared disk to mount before DB access."""
    for _ in range(40):  # ~20 seconds max
        if os.path.isdir("/app/data") and os.path.ismount("/app/data"):
            print("[worker] Shared disk mounted at /app/data")
            return True
        print("[worker] Waiting for /app/data mount...")
        time.sleep(0.5)

    print("[worker] WARNING: Disk never mounted. Using ephemeral FS.")
    return False


def job_generate():
    print("[worker] Running job_generate...")

    wait_for_disk()

    print("[worker] Initializing database...")
    init_db()

    print("[worker] Fetching trends...")
    trends = get_trends()

    print("[worker] Composing drafts...")
    drafts = compose_drafts(trends)

    print("[worker] Saving drafts...")
    save_drafts(drafts)

    print(f"[worker] Saved {len(drafts)} drafts")


def start_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(job_generate, "interval", minutes=1)
    print("[worker] Scheduler started")
    scheduler.start()


if __name__ == "__main__":
    print("[worker] Starting...")
    start_scheduler()
