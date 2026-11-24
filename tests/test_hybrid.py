
from db import get_candidate, get_saved_jobs
from matching import match_jobs
from semantic import calculate_job_similarity

candidate = get_candidate("ananya_resume.docx")
jobs = get_saved_jobs()

# Existing keyword-based matching
matches = match_jobs(candidate["profile"], jobs)

print("\n===== ORIGINAL MATCHING =====")

for match in matches:
    print(
        match["title"],
        "|",
        match["company"],
        "|",
        match["match_score"]
    )


print("\n===== HYBRID EXPERIMENT =====")

# Match each saved job by its database ID.
jobs_by_id = {job["id"]: job for job in jobs}

comparison = []

for match in matches:
    job = jobs_by_id[match["job_id"]]

    semantic_score = calculate_job_similarity(
        candidate["profile"],
        job
    )

    comparison.append({
        "title": match["title"],
        "company": match["company"],
        "original_score": match["match_score"],
        "semantic_score": semantic_score
    })

# Sort by original score for now.
comparison.sort(
    key=lambda item: item["original_score"],
    reverse=True
)

for item in comparison:
    print(
        f'{item["title"]} | '
        f'{item["company"]} | '
        f'Original: {item["original_score"]}/100 | '
        f'Semantic: {item["semantic_score"]:.4f}'
    )


print("\n===== INVESTIGATING SENeca =====")

seneca = next(
    job for job in jobs
    if job.get("company") == "Seneca Global IT Services Pvt Ltd"
)

print("\nCANDIDATE PROFILE:")
print(candidate["profile"])

print("\nSENECA JOB DESCRIPTION:")
print(seneca["description"])
