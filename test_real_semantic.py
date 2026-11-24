
from db import get_candidate, get_saved_jobs
from semantic import calculate_job_similarity

candidate = get_candidate("ananya_resume.docx")
jobs = get_saved_jobs()

for job in jobs[:5]:
    score = calculate_job_similarity(
        candidate["profile"],
        job
    )

    print(
        job["title"],
        "|",
        job["company"],
        "|",
        round(score, 4)
    )
