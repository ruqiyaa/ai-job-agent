from db import get_candidate
from semantic import calculate_job_similarity

candidate = get_candidate("ananya_resume.docx")["profile"]

jobs = [
    {
        "title": "React Developer",
        "description": """
        Build responsive user interfaces using React.js,
        JavaScript, Redux, HTML and CSS.
        Work with REST APIs and Git.
        """
    },
    {
        "title": "Python Developer",
        "description": """
        Develop backend applications using Python,
        Flask, Django, SQLAlchemy and REST APIs.
        Build automation scripts.
        """
    },
    {
        "title": "Full Stack Developer",
        "description": """
        Build frontend components using React.js
        and JavaScript. Develop backend services using
        Python and Flask. Work with Docker and SQLAlchemy.
        """
    }
]

for job in jobs:
    score = calculate_job_similarity(candidate, job)

    print(f"{job['title']}: {score:.4f}")
