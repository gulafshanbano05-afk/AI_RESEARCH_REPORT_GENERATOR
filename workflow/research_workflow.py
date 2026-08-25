import time
from typing import TypedDict, Any
from langgraph.graph import StateGraph, END

from agents.research_agent import research_agent
from agents.outline_agent import outline_agent
from agents.writer_agent import writer_agent
from agents.fact_checker_agent import fact_checker_agent
from agents.citation_agent import citation_agent
from search.search_manager import search_manager


# ============================================================
# WORKFLOW STATE DEFINITION
# ============================================================

class ResearchState(TypedDict):
    topic: str
    search_data: Any
    research_notes: str
    outline: str
    report: str
    fact_check: dict
    citations: list
    iteration_count: int


# ============================================================
# WORKFLOW NODES
# ============================================================

def search_node(state: ResearchState) -> dict:
    topic = state.get("topic", "")
    search_results = search_manager(topic)
    time.sleep(1.2)
    return {"search_data": search_results}


def research_node(state: ResearchState) -> dict:
    topic = state.get("topic", "")
    search_data = state.get("search_data", "")
    notes = research_agent(topic=topic, search_results=search_data)
    time.sleep(1.2)
    return {"research_notes": notes}


def outline_node(state: ResearchState) -> dict:
    topic = state.get("topic", "")
    research_notes = state.get("research_notes", "")
    outline = outline_agent(topic=topic, research_notes=research_notes)
    time.sleep(1.2)
    return {"outline": outline}


def writer_node(state: ResearchState) -> dict:
    topic = state.get("topic", "")
    research_notes = state.get("research_notes", "")
    outline = state.get("outline", "")
    previous_report = state.get("report", "")
    fact_check = state.get("fact_check", None)
    iteration_count = state.get("iteration_count", 0)

    report = writer_agent(
        topic=topic,
        research_notes=research_notes,
        outline=outline,
        previous_report=previous_report,
        fact_check=fact_check
    )
    time.sleep(1.2)
    return {
        "report": report,
        "iteration_count": iteration_count + 1
    }


def fact_checker_node(state: ResearchState) -> dict:
    topic = state.get("topic", "")
    report = state.get("report", "")
    research_notes = state.get("research_notes", "")

    fact_check_result = fact_checker_agent(
        topic=topic,
        report=report,
        research_notes=research_notes
    )
    time.sleep(1.2)
    return {"fact_check": fact_check_result}


def citation_node(state: ResearchState) -> dict:
    topic = state.get("topic", "")
    search_data = state.get("search_data", "")
    report = state.get("report", "")

    citations = citation_agent(
        topic=topic,
        search_data=search_data,
        report=report
    )
    time.sleep(1.2)
    return {"citations": citations}


# ============================================================
# CONDITIONAL ROUTING
# ============================================================

def route_fact_check(state: ResearchState) -> str:
    fact_check = state.get("fact_check", {})
    iteration_count = state.get("iteration_count", 0)

    status = str(fact_check.get("status", "PASS")).upper()

    # If revisions needed and under maximum iterations, loop back to writer
    if status == "REVISE" and iteration_count < 2:
        return "writer"
    
    return "citation"


# ============================================================
# GRAPH COMPILATION
# ============================================================

workflow = StateGraph(ResearchState)

# Add Nodes
workflow.add_node("search", search_node)
workflow.add_node("research", research_node)
workflow.add_node("outline", outline_node)
workflow.add_node("writer", writer_node)
workflow.add_node("fact_checker", fact_checker_node)
workflow.add_node("citation", citation_node)

# Set Entry Point
workflow.set_entry_point("search")

# Add Edges
workflow.add_edge("search", "research")
workflow.add_edge("research", "outline")
workflow.add_edge("outline", "writer")
workflow.add_edge("writer", "fact_checker")

# Conditional Edge for Fact Check Loop
workflow.add_conditional_edges(
    "fact_checker",
    route_fact_check,
    {
        "writer": "writer",
        "citation": "citation"
    }
)

workflow.add_edge("citation", END)

research_workflow = workflow.compile()