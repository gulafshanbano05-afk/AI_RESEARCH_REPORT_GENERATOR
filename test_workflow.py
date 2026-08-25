from workflow.research_workflow import research_workflow


topic = "Machine Learning in Healthcare"


print("======================================")
print("AI RESEARCH REPORT GENERATOR")
print("======================================")

print(f"\nTopic: {topic}")


result = research_workflow.invoke(
    {
        "topic": topic
    }
)


print("\n======================================")
print("FINAL REPORT")
print("======================================")

print(result["report"])


print("\n======================================")
print("FACT CHECK")
print("======================================")

print(result["fact_check"])


print("\n======================================")
print("REFERENCES")
print("======================================")

print(result["citations"])