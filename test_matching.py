
from db import get_candidate, get_saved_jobs
from matching import match_jobs

# 1. Retrieve candidate profile from SQLite
candidate = get_candidate("ananya_resume.pdf")

if candidate is None:
    raise ValueError("Candidate not found!")

# 2. Retrieve saved jobs from SQLite
jobs = get_saved_jobs()

if not jobs:
    raise ValueError("No saved jobs found!")

# 3. Ask Gemini to match candidate with jobs
matches = match_jobs(candidate["profile"], jobs)

# 4. Display ranked results
for match in matches:
    print("\nJob ID:", match["job_id"])
    print("Match score:", match["match_score"], "%")
    print("Matching skills:", match["matched_skills"])
    print("Missing skills:", match["missing_skills"])
    print("Explanation:", match["explanation"])
    print("-" * 50)
