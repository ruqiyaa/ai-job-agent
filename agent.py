
from db import init_db, get_candidate, save_jobs, get_saved_jobs

from job_sources.adzuna import search as search_adzuna
from job_sources.remotive import search as search_remotive

from matching import match_jobs


RESUME_FILENAME = "ruqiya_cv.pdf"
LOCATION = "India"


def run_agent(resume_filename, location):
    init_db()

    candidate = get_candidate(resume_filename)

    if not candidate:
        raise ValueError("Candidate resume not found in database.")

    profile = candidate["profile"]
    search_queries = profile.get("job_titles", [])

    if not search_queries:
        raise ValueError("No job titles found in candidate profile.")

    print("\nJOB AGENT STARTED")
    print("Candidate:", profile["name"])
    print("Search queries:", search_queries)

    discovered_jobs = {}

    for keyword in search_queries:
        print(f"\nSearching Adzuna: {keyword}")

        try:
            results = search_adzuna(keyword, location)

            for job in results:
                discovered_jobs[job["job_url"]] = job

        except Exception as error:
            print("Adzuna search failed:", error)

    for keyword in search_queries:
        print(f"\nSearching Remotive: {keyword}")

        try:
            results = search_remotive(keyword)

            for job in results:
                discovered_jobs[job["job_url"]] = job

        except Exception as error:
            print("Remotive search failed:", error)

    jobs = list(discovered_jobs.values())

    print("\nTotal unique jobs discovered:", len(jobs))

    if not jobs:
        print("No jobs found.")
        return

    saved_count = save_jobs(jobs)
    print("New jobs saved:", saved_count)

    saved_jobs = get_saved_jobs()
    job_urls = set(discovered_jobs.keys())

    relevant_jobs = [
        job for job in saved_jobs
        if job["job_url"] in job_urls
    ]

    matches = match_jobs(profile, relevant_jobs)

    matches.sort(
        key=lambda item: item["match_score"],
        reverse=True
    )

    print("\n===== TOP JOB MATCHES =====")

    for index, match in enumerate(matches[:10], start=1):
        job = next(
            (j for j in relevant_jobs if j["id"] == match["job_id"]),
            {}
        )

        print(f"\n{index}. {match['title']}")
        print("Company:", match["company"])
        print("Source:", job.get("source"))
        print("Match score:", match["match_score"], "/100")
        print("Job link:", job.get("job_url"))

    print("\nJOB AGENT FINISHED")


if __name__ == "__main__":
    run_agent(RESUME_FILENAME, LOCATION)
