from search.search_manager import search_topic
from agents.research_agent import research_agent
from agents.outline_agent import outline_agent


topic = "Artificial Intelligence in Education"

print("Step 1: Searching...")
research_data = search_topic(topic)

print("Step 2: Creating research notes...")
research_notes = research_agent(
    topic,
    research_data
)

print("Step 3: Creating report outline...\n")

outline = outline_agent(
    topic,
    research_notes
)

print("\n==============================")
print("RESEARCH REPORT OUTLINE")
print("==============================")

print(outline)