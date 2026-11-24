
from semantic import compare_texts

candidate = """
Built REST APIs using Flask.
Developed responsive interfaces using React.
"""

job = """
Looking for a developer experienced in Python backend services,
REST API development and web frameworks.
"""

score = compare_texts(candidate, job)

print("Semantic similarity:", round(score, 4))
