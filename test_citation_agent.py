from search.search_manager import search_topic
from agents.research_agent import research_agent
from agents.outline_agent import outline_agent
from agents.writer_agent import writer_agent
from agents.fact_checker_agent import fact_checker_agent
from agents.citation_agent import citation_agent


topic = "Artificial Intelligence in Education"


print("STEP 1: SEARCHING...")
research_data = search_topic(topic)


print("STEP 2: RESEARCH AGENT...")
research_notes = research_agent(
    topic,
    research_data
)


print("STEP 3: OUTLINE AGENT...")
outline = outline_agent(
    topic,
    research_notes
)


print("STEP 4: WRITER AGENT...")
report = writer_agent(
    topic,
    research_notes,
    outline
)


print("STEP 5: FACT CHECKER...")
fact_check = fact_checker_agent(
    topic,
    research_notes,
    report
)


print("STEP 6: CITATION AGENT...")
citations = citation_agent(
    topic,
    research_data,
    research_notes,
    fact_check
)


print("\n======================================")
print("REFERENCES")
print("======================================\n")

print(citations)