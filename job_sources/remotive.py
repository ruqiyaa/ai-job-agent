
import requests
from html import unescape
from html.parser import HTMLParser


class HTMLTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)

    def get_text(self):
        return " ".join(self.parts)


def clean_html(html):
    parser = HTMLTextParser()
    parser.feed(html or "")
    return unescape(parser.get_text())


def search(keyword):
    url = "https://remotive.com/api/remote-jobs"

    response = requests.get(
        url,
        params={
            "search": keyword,
            "limit": 50
        },
        timeout=30
    )

    response.raise_for_status()

    raw_jobs = response.json().get("jobs", [])
    jobs = []

    for job in raw_jobs:
        job_url = job.get("url")

        if not job_url:
            continue

        description = clean_html(job.get("description", ""))

        jobs.append({
            "title": job.get("title") or "Unknown title",
            "company": job.get("company_name"),
            "location": job.get("candidate_required_location") or "Remote",
            "description": description,
            "job_url": job_url,
            "source": "Remotive"
        })

    return jobs
