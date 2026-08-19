from llm.groq_llm import get_llm


def citation_agent(
    topic: str,
    research_data: dict,
    research_notes: str,
    fact_check: str
) -> str:
    """
    Identify and organize the sources used during research.
    """

    llm = get_llm()

    prompt = f"""
You are an academic citation assistant.

Research Topic:
{topic}

Wikipedia Research:
{research_data.get("wikipedia", "")}

Web Search Results:
{research_data.get("tavily", "")}

Research Notes:
{research_notes}

Fact-Checking Results:
{fact_check}

Your task is to create a clean academic references section
using ONLY the sources provided above.

For each source, provide:

1. Source title
2. Website or publisher
3. URL
4. A short description of what information the source supports

Rules:

- Do not invent sources.
- Do not invent URLs.
- Do not invent authors or publication dates.
- Only use sources that appear in the provided research data.
- Remove duplicate sources.
- Prefer sources that directly support the research topic.
- If source information is incomplete, clearly indicate that it is incomplete.

Format the final result as:

REFERENCES

[1] Title — Publisher/Website
URL: ...
Supports: ...

[2] Title — Publisher/Website
URL: ...
Supports: ...

Continue for all useful sources.
"""

    response = llm.invoke(prompt)

    return response.content