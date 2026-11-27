from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

from agents import (
    summarization_agent,
    task_extraction_agent,
    deadline_detection_agent,
    email_generation_agent
)


class MeetingState(TypedDict):
    transcript: str
    summary: Optional[dict]
    tasks: Optional[dict]
    deadlines: Optional[dict]
    email: Optional[dict]


def summarize_node(state: MeetingState):
    result = summarization_agent(state["transcript"])

    return {
        "summary": result.model_dump()
    }


def task_node(state: MeetingState):
    result = task_extraction_agent(state["transcript"])

    return {
        "tasks": result.model_dump()
    }


def deadline_node(state: MeetingState):
    result = deadline_detection_agent(state["transcript"])

    return {
        "deadlines": result.model_dump()
    }


def email_node(state: MeetingState):
    from schemas import (
        MeetingSummary,
        TaskExtraction,
        DeadlineExtraction
    )

    summary = MeetingSummary(**state["summary"])
    tasks = TaskExtraction(**state["tasks"])
    deadlines = DeadlineExtraction(**state["deadlines"])

    result = email_generation_agent(
        state["transcript"],
        summary,
        tasks,
        deadlines
    )

    return {
        "email": result.model_dump()
    }


def build_graph():

    workflow = StateGraph(MeetingState)

    workflow.add_node("summarize", summarize_node)
    workflow.add_node("extract_tasks", task_node)
    workflow.add_node("detect_deadlines", deadline_node)
    workflow.add_node("generate_email", email_node)

    workflow.set_entry_point("summarize")

    workflow.add_edge("summarize", "extract_tasks")
    workflow.add_edge("extract_tasks", "detect_deadlines")
    workflow.add_edge("detect_deadlines", "generate_email")
    workflow.add_edge("generate_email", END)

    return workflow.compile()


meeting_graph = build_graph()


def process_meeting(transcript: str):

    initial_state = {
        "transcript": transcript,
        "summary": None,
        "tasks": None,
        "deadlines": None,
        "email": None
    }

    return meeting_graph.invoke(initial_state)
