from llm.groq_llm import get_llm


def writer_agent(
    topic: str,
    research_notes: str,
    outline: str,
    previous_report: str = "",
    fact_check: dict | None = None
) -> str:
    llm = get_llm()

    # Strict safety caps
    safe_notes = str(research_notes)[:2500]
    safe_outline = str(outline)[:1200]

    if not previous_report or not fact_check:
        prompt = f"""
You are an academic research report writer.

Topic:
{topic}

Research Notes:
{safe_notes}

Outline:
{safe_outline}

Task:
Write a structured academic brief using only the facts provided in the research notes.
Include section headers, an Abstract, Key Findings, and a Brief Conclusion.
Do not invent facts or citations.
"""
    else:
        feedback = fact_check.get("analysis", "Address unsupported claims.")
        prompt = f"""
You are an academic research report editor.

Topic:
{topic}

Research Notes:
{safe_notes}

Previous Report:
{str(previous_report)[:2000]}

Feedback:
{str(feedback)[:1000]}

Task:
Revise the report strictly following the research notes. Remove unsupported claims.
"""

    response = llm.invoke(prompt)
    return response.content