
from db import get_candidate, get_saved_jobs
from matching import match_jobs
import json

candidate = get_candidate("ananya_resume.docx")
jobs = get_saved_jobs()

matches = match_jobs(candidate["profile"], jobs)

print(json.dumps(matches, indent=4))

# for job in jobs:
#     print("\nJOB:", job["id"])
#     print("TITLE:", job["title"])
#     print("COMPANY:", job["company"])
#     print("DESCRIPTION:", (job.get("description") or "")[:300])
