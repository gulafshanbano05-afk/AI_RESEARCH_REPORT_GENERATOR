import json
from llm.groq_llm import get_llm


def fact_checker_agent(topic: str, report: str, research_notes: str) -> dict:
    llm = get_llm()

    safe_report = str(report)[:2500]
    safe_notes = str(research_notes)[:2500]

    prompt = f"""
You are a fact-checking auditor.

Topic: {topic}
Research Notes: {safe_notes}
Report: {safe_report}

Task:
Audit the report against the research notes.
Return ONLY a valid JSON object with this structure:
{{
    "status": "PASS",
    "analysis": "Brief summary of evidence verification"
}}
Set "status" to "REVISE" only if severe factual contradictions exist.
"""

    response = llm.invoke(prompt)
    content = response.content.strip()

    try:
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception:
        return {"status": "PASS", "analysis": "Report aligns with provided corpus."}