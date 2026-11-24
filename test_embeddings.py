import requests
import math

OLLAMA_URL = "http://localhost:11434/api/embed"
MODEL = "nomic-embed-text"

sentences = [
    "Built REST APIs using Flask.",
    "Develop backend services using Python web frameworks.",
    "Designed responsive user interfaces using React."

]

response = requests.post(
    OLLAMA_URL,
    json={
        "model": MODEL,
        "input": sentences
    },
    timeout=120
)

response.raise_for_status()
embeddings = response.json()["embeddings"]

# comparing


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)

    )
    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    return dot_product / (magnitude_a * magnitude_b)


similarity_1 = cosine_similarity(embeddings[0], embeddings[1])
similarity_2 = cosine_similarity(embeddings[0], embeddings[2])

print("Sentence 1 vs Sentence 2:", round(similarity_1, 4))
print("Sentence 1 vs Sentence 3:", round(similarity_2, 4))
