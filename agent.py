from db import (
    init_db,
    get_candidate,
    save_jobs,
    get_saved_jobs
)
from job_search import search_jobs
from matching import match_jobs

# temp settingd
RESUME_FILENAME = "ruqiya_cv.pdf"
LOCATION = "India"


def run_agent(resume_filename, location):
    init_db()

    candidate = get_candidate(resume_filename)

    if not candidate:
        raise ValueError("Candidate not found in db")

    profile = candidate["profile"]
    search_queries = profile.get("job_titles", [])

    if not search_queries:
        raise ValueError("no job titles found in candidate profile")

    print("\nJOB AGENT STARTED")
    print("Candidate:", profile["name"])
    print("Search queries:", search_queries)

    discovered_jobs = {}
    for keyword in search_queries:
        print(f"\nSearching for: {keyword}")

        results = search_jobs(keyword, location)

        for job in results:
            url = job.get("redirect_url")

            if url:
                discovered_jobs[url] = job

    jobs = list(discovered_jobs.values())

    print(f"\nJobs discovered: {len(jobs)}")

    if not jobs:
        print("No jobs found.")
        return

    # 4. Save discovered jobs
    saved_count = save_jobs(jobs)

    print(f"New jobs saved: {saved_count}")

    # 5. Retrieve matching jobs from database
    saved_jobs = get_saved_jobs()

    job_urls = set(discovered_jobs.keys())

    relevant_jobs = [
        job for job in saved_jobs
        if job["job_url"] in job_urls
    ]

    # 6. Match and rank
    matches = match_jobs(profile, relevant_jobs)

    matches.sort(
        key=lambda item: item["match_score"],
        reverse=True
    )

    # 7. Display results
    print("\n===== TOP JOB MATCHES =====")

    for index, match in enumerate(matches, start=1):
        print(f"\n{index}. {match['title']}")
        print("Company:", match["company"])
        print("Match score:", match["match_score"], "/100")
        print("Matched skills:", match["matched_skills"])
        print("Missing skills:", match["missing_skills"])

    print("\nJOB AGENT FINISHED")


if __name__ == "__main__":
    run_agent(RESUME_FILENAME, LOCATION)
