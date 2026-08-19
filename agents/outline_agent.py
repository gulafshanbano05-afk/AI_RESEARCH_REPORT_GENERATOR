from llm.groq_llm import get_llm


def outline_agent(topic: str, research_notes: str) -> str:
    """
    Create a structured research report outline
    from the research notes.
    """

    llm = get_llm()

    prompt = f"""
You are an academic research planning assistant.

Research Topic:
{topic}

Research Notes:
{research_notes}

Based ONLY on the research notes provided above,
create a logical academic research report outline.

The outline should contain:

1. Title
2. Abstract
3. Introduction
4. Background / Related Work
5. Main Discussion
6. Findings
7. Challenges or Limitations
8. Future Scope
9. Conclusion
10. References

For each major section, provide 2-4 useful
subsections that would help another AI agent
write the final report.

Do not invent research findings.
Keep the outline academically structured.
"""

    response = llm.invoke(prompt)

    return response.content