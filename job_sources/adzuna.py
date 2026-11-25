
from job_search import search_jobs


def search(keyword, location="India"):
    raw_jobs = search_jobs(keyword, location)

    jobs = []

    for job in raw_jobs:
        url = job.get("redirect_url")

        if not url:
            continue

        jobs.append({
            "title": job.get("title") or "Unknown title",
            "company": (job.get("company") or {}).get("display_name"),
            "location": (job.get("location") or {}).get("display_name"),
            "description": job.get("description") or "",
            "job_url": url,
            "source": "Adzuna"
        })

    return jobs
