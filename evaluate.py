import json
import os
import pandas as pd

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from graph import process_meeting

load_dotenv()

judge = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0
)


SCENARIOS = [
    "John will finish the sales report by Friday. Sarah will review it.",
    "The team discussed improving customer retention. No tasks were assigned.",
    "Alex will prepare the budget by December 5. Maria will approve it.",
    "We need to deploy the new application next Monday. David owns deployment.",
    "Priya will complete the data cleaning. Rahul will build the dashboard.",
    "The marketing campaign should launch in two weeks. The team will review it tomorrow.",
    "Emma will share the project documentation by Wednesday.",
    "The team decided to postpone the product launch. No deadline was confirmed.",
    "Mike will fix the API issue by tomorrow. Sarah will test the changes.",
    "The team discussed cloud migration. Raj will prepare a proposal by next Friday.",
    "The design team will share mockups next Tuesday. The development team will review them.",
    "No specific tasks or deadlines were assigned during the meeting."
]


def evaluate_output(transcript, output):

    prompt = f"""
    You are an independent evaluator assessing an AI meeting
    intelligence system.

    Evaluate the output against the original transcript.

    ORIGINAL TRANSCRIPT:
    {transcript}

    GENERATED OUTPUT:
    {json.dumps(output, indent=2)}

    Score the system on the following dimensions from 1 to 5:

    1. Summary relevance
    2. Action item extraction accuracy
    3. Deadline extraction accuracy
    4. Faithfulness to the transcript

    Penalize invented tasks, owners, decisions and deadlines.

    Return ONLY valid JSON in this format:

    {{
        "summary_relevance": 1,
        "task_accuracy": 1,
        "deadline_accuracy": 1,
        "faithfulness": 1,
        "reason": "Brief explanation"
    }}
    """

    response = judge.invoke(prompt)

    content = response.content

    if isinstance(content, list):
        content = "".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
        )

    content = content.strip()

    if content.startswith("```"):
        content = content.split("\n", 1)[1].rsplit("```", 1)[0]

    return json.loads(content)


def main():

    results = []

    for index, transcript in enumerate(SCENARIOS, start=1):

        print(f"Evaluating scenario {index}/{len(SCENARIOS)}")

        try:
            output = process_meeting(transcript)

            evaluation = evaluate_output(
                transcript,
                output
            )

            scores = [
                evaluation["summary_relevance"],
                evaluation["task_accuracy"],
                evaluation["deadline_accuracy"],
                evaluation["faithfulness"]
            ]

            results.append({
                "scenario": index,
                **evaluation,
                "average_score": sum(scores) / len(scores)
            })

        except Exception as error:
            print(f"Scenario {index} failed: {error}")

    if not results:
        print("No scenarios were evaluated successfully.")
        return

    df = pd.DataFrame(results)

    df.to_csv(
        "evaluation_results.csv",
        index=False
    )

    print("\nEvaluation Results")
    print(df.to_string(index=False))

    print("\nAverage Evaluation Score:")
    print(
        round(df["average_score"].mean(), 2),
        "/ 5"
    )


if __name__ == "__main__":
    main()
