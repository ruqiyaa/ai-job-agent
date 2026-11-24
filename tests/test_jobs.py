
from job_search import search_jobs
from db import init_db, save_jobs

init_db()

jobs = search_jobs("Python Developer", "Hyderabad")
saved_count = save_jobs(jobs)

for job in jobs:
    company = job.get("company") or {}
    location = job.get("location") or {}

    print("Title:", job.get("title", "Not specified"))
    print("Company:", company.get("display_name", "Not specified"))
    print("Location:", location.get("display_name", "Not specified"))
    print("URL:", job.get("redirect_url", "Not available"))
    print("-" * 40)

    print(f"\nSaved--------------\n{saved_count} new jobs at db")
