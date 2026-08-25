import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import WikipediaAPIWrapper

load_dotenv()


def search_manager(topic: str) -> dict:
    """
    Collects research data from Wikipedia and Tavily web search.
    """
    results = {
        "wiki_data": "",
        "web_data": []
    }

    # 1. Wikipedia Search
    try:
        wiki = WikipediaAPIWrapper(
            top_k_results=2,
            doc_content_chars_max=2000
        )
        results["wiki_data"] = wiki.run(topic)
    except Exception as e:
        results["wiki_data"] = f"Wikipedia search unavailable: {str(e)}"

    # 2. Tavily Web Search
    tavily_api_key = os.getenv("TAVILY_API_KEY")

    if tavily_api_key:
        try:
            tavily_tool = TavilySearchResults(
                max_results=3,
                tavily_api_key=tavily_api_key
            )
            results["web_data"] = tavily_tool.invoke({"query": topic})
        except Exception as e:
            results["web_data"] = [{"content": f"Tavily search error: {str(e)}"}]
    else:
        results["web_data"] = [{"content": "TAVILY_API_KEY not configured."}]

    return results