from search.search_manager import search_topic
from agents.research_agent import research_agent
from agents.outline_agent import outline_agent
from agents.writer_agent import writer_agent


topic = "Artificial Intelligence in Education"


print("======================================")
print("STEP 1: SEARCHING")
print("======================================")

research_data = search_topic(topic)


print("\n======================================")
print("STEP 2: RESEARCH AGENT")
print("======================================")

research_notes = research_agent(
    topic,
    research_data
)


print("\n======================================")
print("STEP 3: OUTLINE AGENT")
print("======================================")

outline = outline_agent(
    topic,
    research_notes
)


print("\n======================================")
print("STEP 4: WRITER AGENT")
print("======================================")

report = writer_agent(
    topic,
    research_notes,
    outline
)


print("\n======================================")
print("FINAL RESEARCH REPORT")
print("======================================\n")

print(report)