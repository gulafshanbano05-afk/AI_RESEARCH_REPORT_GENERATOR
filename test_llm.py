from llm.groq_llm import get_llm


llm = get_llm()

response = llm.invoke(
    "Explain artificial intelligence in simple language."
)

print(response.content)