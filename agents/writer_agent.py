from llm.groq_llm import get_llm


def writer_agent(
    topic: str,
    research_notes: str,
    outline: str,
    previous_report: str = "",
    fact_check: dict | None = None
) -> str:
    """
    Generate a research report.

    If a previous report and fact-check result are provided,
    revise the report according to the identified issues.
    """

    llm = get_llm()

    # ==========================================
    # FIRST REPORT GENERATION
    # ==========================================

    if not previous_report or not fact_check:

        prompt = f"""
You are an academic research report writer.

Research Topic:
{topic}

Research Notes:
{research_notes}

Approved Report Outline:
{outline}

Your task is to write a complete, well-structured
research report based ONLY on the information provided.

IMPORTANT RULES:

1. Follow the approved outline.
2. Use the research notes as the primary source of information.
3. Do not invent statistics, studies, facts, or citations.
4. Do not make unsupported claims.
5. If the research notes do not provide enough evidence
   for a point, do not present that point as a fact.
6. Use clear formal academic English.
7. Give every major section a heading.
8. Develop each section with meaningful paragraphs.
9. Maintain logical flow between sections.
10. Include a conclusion that summarizes the findings.
11. Do not include a separate references section unless
    references are explicitly present in the research notes.

Write only the research report.
"""

    # ==========================================
    # REPORT REVISION
    # ==========================================

    else:

        fact_check_analysis = fact_check.get(
            "analysis",
            "No detailed feedback was provided."
        )

        prompt = f"""
You are an academic research report editor.

The report below has already been generated and
was reviewed by a fact-checking agent.

Your job is to REVISE the report so that the
identified unsupported or questionable claims
are corrected.

Research Topic:
{topic}

Research Notes:
{research_notes}

Approved Report Outline:
{outline}

PREVIOUS REPORT:
{previous_report[:8000]}

FACT-CHECKER FEEDBACK:
{fact_check_analysis}

IMPORTANT REVISION RULES:

1. Preserve the overall structure and useful content
   of the previous report.
2. Address EVERY issue identified by the fact checker.
3. Remove claims that are not supported by the
   research notes.
4. Rewrite unsupported claims only when the research
   notes provide sufficient evidence.
5. Do not invent new facts, statistics, studies,
   citations, or evidence.
6. Do not use outside knowledge to fill evidence gaps.
7. If a claim cannot be supported by the research notes,
   remove it or replace it with a carefully supported
   statement.
8. Keep the report academically written and coherent.
9. Do not mention the fact-checking process in the report.
10. Do not add a separate references section unless
    references are explicitly present in the research notes.

Return ONLY the revised research report.
"""

    response = llm.invoke(prompt)

    return response.content