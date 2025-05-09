import requests
import os

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def analyze_resume(resume_text: str) -> dict:
    prompt = f"""
You are a Resume Analyzer Agent.
Extract the following:
- Name
- Skills (list)
- Years of Experience
- Education
- Top 3 strengths

Resume:
{resume_text}
"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print(f"Response content: {response.text}")
        return {"error": f"API request failed with status code {response.status_code}"}

    try:
        return parse_response(response.json()["choices"][0]["message"]["content"])
    except (KeyError, IndexError) as e:
        print(f"Error parsing response: {e}")
        print(f"Full response: {response.json()}")
        return {"error": "Unexpected response format from API"}

def parse_response(text: str) -> dict:
    from ast import literal_eval
    try:
        return literal_eval(text) if "{" in text else {"raw": text}
    except:
        return {"raw": text}

def match_roles(skills: list, jobs: list):
    results = []
    for job in jobs:
        score = len(set(skills) & set(job["required_skills"]))
        if score > 0:
            results.append({"job": job, "match_score": score})
    return sorted(results, key=lambda x: x["match_score"], reverse=True)