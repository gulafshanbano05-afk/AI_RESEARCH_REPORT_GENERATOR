from llm.groq_llm import get_llm


def research_agent(topic: str, search_results: dict | list | str) -> str:
    llm = get_llm()

    # Strict token cap on raw search results
    safe_search = str(search_results)[:3500]

    prompt = f"""
You are an academic research analyst.

Topic:
{topic}

Raw Search Data:
{safe_search}

Task:
Extract key facts, statistics, and verifiable findings into clear bullet points.
Be concise, strictly factual, and do not invent information.

Research Notes:
"""

    response = llm.invoke(prompt)
    return response.content