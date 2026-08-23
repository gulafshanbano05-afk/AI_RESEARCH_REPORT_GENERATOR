import os

import wikipedia
from tavily import TavilyClient
from dotenv import load_dotenv


load_dotenv()


def search_wikipedia(topic: str) -> list:
    """Search Wikipedia and return structured source information."""

    try:
        results = wikipedia.search(topic)

        if not results:
            return []

        page = wikipedia.page(
            results[0],
            auto_suggest=False
        )

        return [
            {
                "title": page.title,
                "publisher": "Wikipedia",
                "url": page.url,
                "content": page.summary
            }
        ]

    except Exception as e:
        print(f"⚠️ Wikipedia search failed: {e}")
        return []


def search_tavily(topic: str) -> list:
    """Search the web using Tavily and return structured sources."""

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError(
            "TAVILY_API_KEY is not set in the .env file."
        )

    client = TavilyClient(api_key=api_key)

    response = client.search(
        query=topic,
        max_results=5
    )

    results = response.get("results", [])

    if not results:
        return []

    sources = []

    for result in results:

        sources.append(
            {
                "title": result.get("title", ""),
                "publisher": "Web Search",
                "url": result.get("url", ""),
                "content": result.get("content", "")
            }
        )

    return sources


def search_topic(topic: str) -> dict:
    """Run Wikipedia and Tavily searches."""

    wikipedia_sources = search_wikipedia(topic)
    tavily_sources = search_tavily(topic)

    return {
        "topic": topic,
        "sources": wikipedia_sources + tavily_sources
    }