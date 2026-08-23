from llm.groq_llm import get_llm


def fact_checker_agent(
    topic: str,
    research_notes: str,
    report: str
) -> dict:
    """
    Check the generated report against the available
    research evidence and decide whether revision is needed.
    """

    llm = get_llm()

    prompt = f"""
You are an academic fact checker.

Topic:
{topic}

RESEARCH EVIDENCE:
{research_notes}

REPORT TO CHECK:
{report}

TASK:
Compare the report ONLY against the research evidence provided.

Find important claims in the report that are:
- unsupported by the research evidence
- contradictory to the research evidence
- questionable because the evidence is insufficient

Do NOT use outside knowledge.

Return ONLY this format:

STATUS: PASS

ISSUES:
None

OR:

STATUS: REVISE

ISSUES:
1. [unsupported/questionable claim]
2. [unsupported/questionable claim]

RULES:
- PASS if the important claims are reasonably supported.
- REVISE only when an important factual issue exists.
- Ignore grammar, wording, style, and minor repetition.
- Do not invent evidence.
- Keep the response concise.
- List at most 3 important issues.
"""

    response = llm.invoke(prompt)

    result = response.content.strip()

    if "STATUS: REVISE" in result:
        status = "REVISE"
    else:
        status = "PASS"

    return {
        "status": status,
        "analysis": result
    }