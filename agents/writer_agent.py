from llm.groq_llm import get_llm


def writer_agent(
    topic: str,
    research_notes: str,
    outline: str
) -> str:
    """
    Generate a complete research report using
    research notes and the approved outline.
    """

    llm = get_llm()

    prompt = f"""
You are an academic research report writer.

Research Topic:
{topic}

Research Notes:
{research_notes}

Approved Report Outline:
{outline}

Your task is to write a complete, well-structured
research report based on the information provided.

IMPORTANT RULES:

1. Follow the approved outline.
2. Use the research notes as the primary source of information.
3. Do not invent statistics, studies, facts, or citations.
4. Do not make unsupported claims.
5. Use clear formal academic English.
6. Give every major section a heading.
7. Develop each section with meaningful paragraphs.
8. Maintain logical flow between sections.
9. Include a conclusion that summarizes the findings.
10. Do not include a separate references section unless
    references are explicitly present in the research notes.

Write only the research report.
"""

    response = llm.invoke(prompt)

    return response.content