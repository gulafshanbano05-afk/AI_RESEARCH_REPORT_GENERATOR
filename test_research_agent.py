from search.search_manager import search_topic
from agents.research_agent import research_agent


topic = "Artificial Intelligence in Education"

print("Searching for research information...")

research_data = search_topic(topic)

print("Research data collected.")
print("Generating research notes...\n")

research_notes = research_agent(
    topic,
    research_data
)

print("\n==============================")
print("RESEARCH NOTES")
print("==============================")

print(research_notes)