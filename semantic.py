import requests
import math

OLLAMA_URL = "http://localhost:11434/api/embed"
MODEL = "nomic-embed-text"


def get_embeddings(texts):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "input": texts
        },
        timeout=120
    )
    response.raise_for_status()
    return response.json()["embeddings"]


def cosine_similarity(vector_a, vector_b):
    """Measure how similar two vectors are."""

    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def compare_texts(text_a, text_b):
    embeddings = get_embeddings([text_a, text_b])
    return cosine_similarity(
        embeddings[0],
        embeddings[1]
    )


def calculate_job_similarity(candidate_profile, job):

    candidate_text = f"""
    Experience: {candidate_profile.get('experience', '')}
    Skills: {', '.join(candidate_profile.get('skills', []))}
    Job titles: {', '.join(candidate_profile.get('job_titles', []))}
    Education: {', '.join(candidate_profile.get('education', []))}
    """

    job_text = f"""
    Job title: {job.get('title', '')}
    Company: {job.get('company', '')}
    Description: {job.get('description', '')}
    """

    return compare_texts(candidate_text, job_text)
