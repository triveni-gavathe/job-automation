from groq import Groq
from django.conf import settings
client=Groq(api_key=settings.GROQ_API_KEY)



def analyze_resume(resume_text):
    prompt = f"""
You are an expert HR recruiter and resume coach.
Analyze the following resume and respond ONLY in JSON format.
No extra text. Just JSON.

{{
  "score": <number out of 100>,
  "strengths": [<3 specific strengths as strings>],
  "weaknesses": [<3 specific weaknesses as strings>],
  "improvements": [<5 actionable improvements as strings>],
  "missing_keywords": [<5 important keywords missing as strings>],
  "summary": "<2 line overall summary>"
}}

Resume:
{resume_text}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def match_resume_jd(resume_text, jd_text):
    prompt = f"""
You are an expert HR recruiter.
Compare this resume against the job description.
Respond ONLY in JSON format. No extra text. Just JSON.

{{
  "match_score": <percentage as number>,
  "matching_skills": [<skills that match as strings>],
  "missing_skills": [<required skills missing as strings>],
  "recommendation": "<one line advice>"
}}

Resume:
{resume_text}

Job Description:
{jd_text}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content