from llm.groq_llm import get_llm


def research_agent(topic: str, research_data: dict) -> str:
    """
    Analyze structured search results and create
    evidence-based research notes.
    """

    llm = get_llm()

    sources = research_data.get("sources", [])

    prompt = f"""
You are a professional research assistant.

Research Topic:
{topic}

========================================
RETRIEVED RESEARCH SOURCES
========================================

{sources}

========================================
TASK
========================================

Analyze ONLY the retrieved research sources above
and create structured research notes.

Include:

1. Introduction
2. Key Concepts
3. Important Findings
4. Supporting Evidence
5. Potential Research Questions
6. Important Sources

IMPORTANT RULES:

1. Use ONLY information contained in the retrieved sources.
2. Do not use outside knowledge.
3. Do not invent facts, statistics, studies, or claims.
4. Do not assume that a source supports something unless
   its provided content supports it.
5. Clearly distinguish between information directly supported
   by a source and reasonable interpretation.
6. Preserve important source details such as title and URL.
7. When evidence is insufficient, explicitly state:
   "Insufficient evidence in the retrieved sources."
8. Do not create sources that are not present in the
   retrieved source list.
9. Keep the research notes organized and concise.
10. Write in clear academic language.

The research notes will be passed to other agents,
so factual accuracy and source traceability are more
important than adding extra information.

Write ONLY the structured research notes.
"""

    response = llm.invoke(prompt)

    return response.content