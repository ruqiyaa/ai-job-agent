
from db import get_candidate
from matching import match_jobs
import json

candidate = get_candidate("ananya_resume.docx")

# A sample frontend job for testing.
frontend_job = {
    "id": 999,
    "title": "Frontend Developer",
    "company": "Test Company",
    "description": """
        We are looking for a Frontend Developer.

        Required skills:
        JavaScript, React.js, HTML5, CSS3, Redux, REST APIs and Git.

        Candidates should have 3 years of experience.
        A B.Tech degree in Computer Science is preferred.
    """
}

matches = match_jobs(
    candidate["profile"],
    [frontend_job]
)

print(json.dumps(matches, indent=4))
