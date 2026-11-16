# Job Agent

An AI-powered job search assistant that helps candidates discover relevant opportunities based on their skills and experience.

Job Agent aims to simplify the job search process by analyzing resumes, finding suitable job openings, tailoring resumes for specific roles, and assisting with applications.

## Current Features

- **Resume Parsing:** Extracts text from PDF and DOCX resumes.
- **AI Resume Analysis:** Uses Google Gemini to analyze resumes.
- **Skill Extraction:** Identifies technical skills, experience, education, projects, certifications, and relevant job titles.
- **Structured Candidate Profile:** Converts resume information into structured JSON data.

## Tech Stack

- **Language:** Python
- **AI:** Google Gemini API
- **Resume Processing:** PyMuPDF, python-docx
- **Environment Management:** Python Virtual Environment
- **Configuration:** python-dotenv

## Project Structure

```text
job-agent/
├── sample_data/
│   └── ananya_resume.pdf
├── resumes/
├── main.py
├── test_gemini.py
├── requirements.txt
├── .gitignore
└── .env
```

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd job-agent
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Get an API key from [Google AI Studio](https://aistudio.google.com/).

### 5. Run the application

```bash
python main.py
```

## Roadmap

- [x] Read PDF and DOCX resumes
- [x] Integrate Google Gemini API
- [x] Extract candidate information using AI
- [x] Generate structured candidate profiles
- [ ] Store candidate profiles using SQLite
- [ ] Search for relevant job openings
- [ ] Match jobs based on candidate skills and experience
- [ ] Generate tailored resumes for individual job descriptions
- [ ] Assist with job applications
- [ ] Send application status notifications

## Note

This project is currently under development. The goal is to build a practical AI-powered job search assistant, with human approval before submitting job applications.# ai-job-agent
