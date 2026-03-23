from google import genai
from django.conf import settings
client=genai.Client(api_key=settings.GEMINI_API_KEY)

def analye_resume(resume_text):
    prompt=f"""
    you are an expert HR recuriter and resume coach
    analyze the following resume and respond only in json format
    no extra text. just JSON
    {{
        "score":[<3 specific stengths as strings>],
        "weaknesses":[<3 specific weaknesses as strings>],
        "improvements":[<5 actinable improvment as strings >],
        "missing_keyword":[<5 important keyword missing as strings>],
        "summary":<2 line overall summary>"
    }}
    
    Resume:
    {resume_text}
    """
    response=client.models.generate_content(
        model="gemini-2.0-flash-lite",
        content=prompt
    )
    return response.text
def match_resume_jd(resume_text,jd_text):
    prompt=f"""
    you are an expert HR recuriter,
    compare this resume againts the job decription.
    Respond ONLY  in JSON format.no extra text .just JSON.
    {{
        "match_score":<percentage as number>,
        "matching_skils":[<skils that as strings>]
        "missing_skils":[<requrired skils missing as stirngs>]
        "recommendation":"<onr line adivce>"RecursionError
    }}
    Resume:
    {resume_text}
    JOb Decription:
    {jd_text}
    """
    response=client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    return resume_text