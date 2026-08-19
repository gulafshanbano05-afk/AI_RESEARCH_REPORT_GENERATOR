from llm.groq_llm import get_llm


def research_agent(topic: str, research_data: dict) -> str:
    """
    Analyze raw search results and create structured research notes.
    """

    llm = get_llm()

    prompt = f"""
You are a professional research assistant.

Research Topic:
{topic}

Wikipedia Information:
{research_data.get("wikipedia", "")}

Web Search Results:
{research_data.get("tavily", "")}

Your task is to analyze the information above and create
structured research notes.

Include:

1. Introduction
2. Key Concepts
3. Important Findings
4. Supporting Evidence
5. Potential Research Questions
6. Important Sources

Do not invent facts that are not supported by the provided
research information.

Write the result in clear academic language.
"""

    response = llm.invoke(prompt)

    return response.content