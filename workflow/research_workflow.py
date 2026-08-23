from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from search.search_manager import search_topic
from agents.research_agent import research_agent
from agents.outline_agent import outline_agent
from agents.writer_agent import writer_agent
from agents.fact_checker_agent import fact_checker_agent
from agents.citation_agent import citation_agent


# ==========================================
# 1. DEFINE THE WORKFLOW STATE
# ==========================================

class ResearchState(TypedDict, total=False):
    topic: str
    research_data: dict
    research_notes: str
    outline: str
    report: str
    fact_check: dict
    citations: str
    revision_count: int


# ==========================================
# 2. SEARCH NODE
# ==========================================

def search_node(state: ResearchState):

    print("\n🔎 SEARCH MANAGER")

    topic = state["topic"]

    research_data = search_topic(topic)

    return {
        "research_data": research_data
    }


# ==========================================
# 3. RESEARCH NODE
# ==========================================

def research_node(state: ResearchState):

    print("\n🧠 RESEARCH AGENT")

    topic = state["topic"]
    research_data = state["research_data"]

    notes = research_agent(
        topic,
        research_data
    )

    return {
        "research_notes": notes
    }


# ==========================================
# 4. OUTLINE NODE
# ==========================================

def outline_node(state: ResearchState):

    print("\n📋 OUTLINE AGENT")

    topic = state["topic"]
    research_notes = state["research_notes"]

    outline = outline_agent(
        topic,
        research_notes
    )

    return {
        "outline": outline
    }


# ==========================================
# 5. WRITER NODE
# ==========================================

def writer_node(state: ResearchState):

    revision_count = state.get("revision_count", 0)

    if revision_count > 0:
        print(f"\n✍️ WRITER AGENT — REVISION {revision_count}")
    else:
        print("\n✍️ WRITER AGENT")

    topic = state["topic"]
    research_notes = state["research_notes"]
    outline = state["outline"]

    # Get previous report and fact-check feedback
    previous_report = state.get("report", "")
    fact_check = state.get("fact_check")

    report = writer_agent(
        topic,
        research_notes,
        outline,
        previous_report,
        fact_check
    )

    return {
        "report": report
    }


# ==========================================
# 6. FACT CHECKER NODE
# ==========================================

def fact_checker_node(state: ResearchState):

    print("\n🔍 FACT CHECKER")

    topic = state["topic"]
    research_notes = state["research_notes"]
    report = state["report"]

    fact_check = fact_checker_agent(
        topic,
        research_notes,
        report
    )

    revision_count = state.get("revision_count", 0)

    status = fact_check.get("status", "PASS")

    print(f"   Status: {status}")

    return {
        "fact_check": fact_check,
        "revision_count": revision_count
    }

# ==========================================
# 7. FACT CHECK ROUTER
# ==========================================

def fact_check_router(state: ResearchState):

    fact_check = state["fact_check"]
    revision_count = state.get("revision_count", 0)

    status = fact_check.get("status", "PASS")

    if status == "PASS":

        print("\n✅ FACT CHECK PASSED")
        return "citation"

    if status == "REVISE" and revision_count < 2:

        next_revision = revision_count + 1

        print(
            f"\n🔄 REVISION REQUIRED "
            f"(Attempt {next_revision}/2)"
        )

        state["revision_count"] = next_revision

        return "writer"

    print("\n⚠️ Maximum revisions reached")
    print("Proceeding to citation.")

    return "citation"


# ==========================================
# 7. CITATION NODE
# ==========================================

def citation_node(state: ResearchState):

    print("\n📚 CITATION AGENT")

    topic = state["topic"]
    research_data = state["research_data"]
    research_notes = state["research_notes"]
    fact_check = state["fact_check"]

    citations = citation_agent(
        topic,
        research_data,
        research_notes,
        fact_check
    )

    return {
        "citations": citations
    }


# ==========================================
# 8. CREATE GRAPH
# ==========================================

graph = StateGraph(ResearchState)


# Add nodes

graph.add_node("search", search_node)
graph.add_node("research", research_node)
graph.add_node("outline", outline_node)
graph.add_node("writer", writer_node)
graph.add_node("fact_checker", fact_checker_node)
graph.add_node("citation", citation_node)


# ==========================================
# 9. CONNECT NODES
# ==========================================

graph.add_edge(START, "search")

graph.add_edge("search", "research")

graph.add_edge("research", "outline")

graph.add_edge("outline", "writer")

graph.add_edge("writer", "fact_checker")

graph.add_conditional_edges(
    "fact_checker",
    fact_check_router,
    {
        "writer": "writer",
        "citation": "citation"
    }
)

graph.add_edge("citation", END)


# ==========================================
# 10. COMPILE GRAPH
# ==========================================

research_workflow = graph.compile()