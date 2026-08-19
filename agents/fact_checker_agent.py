from llm.groq_llm import get_llm


def fact_checker_agent(
    topic: str,
    research_notes: str,
    report: str
) -> str:
    """
    Check the generated report against the available
    research information.
    """

    llm = get_llm()

    prompt = f"""
You are a careful academic fact-checking assistant.

Research Topic:
{topic}

Research Notes:
{research_notes}

Generated Research Report:
{report}

Your task is to fact-check the generated report
against the provided research notes.

For every important claim:

1. Determine whether it is supported by the research.
2. Identify claims that are unsupported or questionable.
3. Identify statements that may be misleading.
4. Suggest corrections when the research supports a correction.

Return your analysis using this structure:

FACT CHECK SUMMARY

Overall Assessment:
[Write a short assessment]

SUPPORTED CLAIMS:
- Claim:
- Evidence:

QUESTIONABLE OR UNSUPPORTED CLAIMS:
- Claim:
- Problem:
- Suggested correction:

MISSING INFORMATION:
- Information that should be added if supported by the research.

IMPORTANT RULE:
Do not use outside knowledge to prove a claim.
Only use the research notes provided above.
If the research notes do not contain enough evidence,
say "Insufficient evidence in provided research."

Do not rewrite the entire report.
Only provide the fact-checking analysis.
"""

    response = llm.invoke(prompt)

    return response.content