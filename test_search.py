from search.search_manager import search_topic


topic = "Artificial Intelligence in Education"

results = search_topic(topic)

print("\n==============================")
print("TOPIC")
print("==============================")
print(results["topic"])

print("\n==============================")
print("WIKIPEDIA")
print("==============================")
print(results["wikipedia"])

print("\n==============================")
print("TAVILY")
print("==============================")
print(results["tavily"])