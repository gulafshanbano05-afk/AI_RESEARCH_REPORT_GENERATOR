from llm.groq_llm import get_llm


def citation_agent(
    topic: str,
    research_data: dict,
    research_notes: str,
    fact_check: dict
) -> str:
    """
    Identify and organize the sources used during research.

    The citation agent only uses source information that was
    actually returned by the research/search stage.
    """

    llm = get_llm()

    sources = research_data.get("sources", [])

    prompt = f"""
You are an academic citation specialist.

Your task is to create a reliable references section
for a research report.

Research Topic:
{topic}

========================================
RETRIEVED SOURCES
========================================

{sources}

========================================
RESEARCH NOTES
========================================

{research_notes}

========================================
FACT-CHECKING RESULTS
========================================

{fact_check}

========================================
STRICT SOURCE RULES
========================================

1. Use ONLY sources explicitly present in the
   retrieved sources above.

2. NEVER invent a source.

3. NEVER invent a URL.

4. NEVER guess a URL from a source title.

5. NEVER invent an author.

6. NEVER invent a publication date.

7. Do not use your general knowledge to add sources.

8. Do not cite a source simply because it is famous
   or relevant. It must appear in the retrieved sources.

9. Remove duplicate sources.

10. If a source does not contain enough information
    to identify its URL, write:

    URL: Not available in retrieved source data

11. If the publisher is unavailable, write:

    Publisher: Not available

12. If the title is unavailable, write:

    Title: Not available

13. The "Supports" description must only describe
    information supported by the retrieved source.

14. Do not introduce new facts while writing
    the source descriptions.

========================================
OUTPUT FORMAT
========================================

REFERENCES

[1] Title — Publisher/Website
URL: ...
Supports: ...

[2] Title — Publisher/Website
URL: ...
Supports: ...

Continue for all useful unique sources.

Return ONLY the REFERENCES section.
"""

    response = llm.invoke(prompt)

    return response.content