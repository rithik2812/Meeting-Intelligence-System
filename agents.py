import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from schemas import (
    MeetingSummary,
    TaskExtraction,
    DeadlineExtraction,
    FollowUpEmail
)

from prompts import (
    SUMMARY_PROMPT,
    TASK_PROMPT,
    DEADLINE_PROMPT,
    EMAIL_PROMPT
)

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0
)


def run_agent(output_schema, system_prompt, user_input):
    """Run an agent and return structured output."""

    structured_llm = llm.with_structured_output(output_schema)

    return structured_llm.invoke([
        ("system", system_prompt),
        ("human", user_input)
    ])


def summarization_agent(transcript):
    return run_agent(
        MeetingSummary,
        SUMMARY_PROMPT,
        transcript
    )


def task_extraction_agent(transcript):
    return run_agent(
        TaskExtraction,
        TASK_PROMPT,
        transcript
    )


def deadline_detection_agent(transcript):
    return run_agent(
        DeadlineExtraction,
        DEADLINE_PROMPT,
        transcript
    )


def email_generation_agent(transcript, summary, tasks, deadlines):

    context = f"""
    ORIGINAL TRANSCRIPT:
    {transcript}

    MEETING SUMMARY:
    {summary.model_dump_json(indent=2)}

    ACTION ITEMS:
    {tasks.model_dump_json(indent=2)}

    DEADLINES:
    {deadlines.model_dump_json(indent=2)}
    """

    return run_agent(
        FollowUpEmail,
        EMAIL_PROMPT,
        context
    )
