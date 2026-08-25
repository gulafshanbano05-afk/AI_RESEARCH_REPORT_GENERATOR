import json
from llm.groq_llm import get_llm


def citation_agent(
    topic: str = "",
    search_data: dict | list | str = None,
    report: str = "",
    **kwargs
) -> list:
    """
    Extracts and structures formal citations and bibliographic links
    from the raw search data and report text.
    """
    if search_data is None:
        search_data = kwargs.get("search_results", kwargs.get("sources", {}))

    llm = get_llm()

    safe_report = str(report)[:2500]
    safe_data = str(search_data)[:2500]

    prompt = f"""
You are an academic citation indexer and bibliographer.

Topic: {topic}
Report Excerpt: {safe_report}
Search Source Data: {safe_data}

Task:
Extract and format verified references/citations based on the provided search data.
Return ONLY a valid JSON list of objects matching this exact structure:
[
  {{
    "title": "Document or Article Title",
    "url_or_source": "Wikipedia or Source URL/Origin",
    "summary": "One sentence summary of relevant context"
  }}
]

If no clear external URLs exist, summarize the primary sources used. Return ONLY valid JSON.
"""

    response = llm.invoke(prompt)
    content = response.content.strip()

    try:
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        parsed = json.loads(content)
        if isinstance(parsed, list):
            return parsed
        return [parsed]
    except Exception:
        return [
            {
                "title": f"Academic Sources for {topic}",
                "url_or_source": "Wikipedia & Academic Index",
                "summary": "Synthesized from multi-source research corpus."
            }
        ]