import os

import wikipedia
from tavily import TavilyClient
from dotenv import load_dotenv


load_dotenv()


def search_wikipedia(topic: str) -> str:
    """Search Wikipedia for background information."""

    try:
        results = wikipedia.search(topic)

        if not results:
            return "No Wikipedia results found."

        page = wikipedia.page(results[0], auto_suggest=False)

        return page.summary

    except Exception as e:
        return f"Wikipedia search failed: {e}"


def search_tavily(topic: str) -> str:
    """Search the web using Tavily."""

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError("TAVILY_API_KEY is not set in the .env file.")

    client = TavilyClient(api_key=api_key)

    response = client.search(
        query=topic,
        max_results=5
    )

    results = response.get("results", [])

    if not results:
        return "No Tavily results found."

    formatted_results = []

    for result in results:
        formatted_results.append(
            f"Title: {result.get('title')}\n"
            f"URL: {result.get('url')}\n"
            f"Content: {result.get('content')}\n"
        )

    return "\n---\n".join(formatted_results)


def search_topic(topic: str) -> dict:
    """Run both Wikipedia and Tavily searches."""

    wikipedia_result = search_wikipedia(topic)
    tavily_result = search_tavily(topic)

    return {
        "topic": topic,
        "wikipedia": wikipedia_result,
        "tavily": tavily_result
    }