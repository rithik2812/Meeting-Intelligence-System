# 🧠 AI-Powered Meeting Intelligence System

An AI-powered multi-agent system that transforms unstructured meeting transcripts into structured summaries, actionable tasks, deadlines, and professional follow-up emails.

Built using **LangGraph, LangChain, OpenAI APIs, Pydantic, and Streamlit**, the application uses specialized AI agents organized into a state-driven workflow to analyze meeting conversations and extract actionable insights.

---

## 🚀 Overview

Meetings often contain important decisions, assigned responsibilities, deadlines, and follow-up requirements buried within lengthy conversations.

Manually reviewing transcripts and identifying these details can be time-consuming.

This project addresses that challenge by building an AI-powered meeting intelligence application that automatically processes meeting transcripts and generates structured outputs.

The system takes a meeting transcript as input and produces:

- 📝 **Meeting Summaries:** Generates concise summaries, meeting titles, key discussion points, and decisions.
- ✅ **Action Item Extraction:** Identifies tasks, descriptions, assigned owners, and initial status.
- 📅 **Deadline Detection:** Extracts deadlines, associated tasks, responsible individuals, original deadline references, and confidence levels.
- ✉️ **Follow-up Email Generation:** Generates professional follow-up emails based on meeting discussions, decisions, tasks, and deadlines.
- 📊 **Structured Outputs:** Presents results in an organized dashboard and supports downloading the complete analysis in JSON format.

---

## ✨ Key Features

### 1. Intelligent Meeting Summarization

The summarization agent processes the original transcript and generates:

- A meaningful meeting title.
- A concise summary of the discussion.
- Important discussion points.
- Decisions explicitly made during the meeting.

The agent distinguishes confirmed decisions from suggestions and avoids introducing unsupported information.

### 2. Automated Action Item Extraction

The task extraction agent identifies actionable responsibilities discussed during the meeting.

For every extracted action item, the system identifies:

- Task description.
- Responsible person, when explicitly mentioned.
- Initial task status.

Tasks are assigned a default status of `Pending`, while unknown owners are represented as `null`.

### 3. Deadline Detection

The deadline detection agent identifies time commitments and deadlines mentioned in the transcript.

For each detected deadline, the system extracts:

- Associated task.
- Responsible person, when available.
- Deadline.
- Original deadline phrase from the transcript.
- Confidence level: High, Medium, or Low.

The system preserves ambiguous deadline references rather than inventing specific dates.

### 4. Automated Follow-up Email Generation

The email generation agent uses the original transcript and previously generated structured outputs to prepare a professional follow-up email.

The generated email includes:

- Email subject.
- Meeting outcomes.
- Action items and responsible individuals.
- Relevant deadlines.

### 5. Interactive Streamlit Dashboard

The application provides an interactive interface where users can:

- Enter meeting transcripts.
- Run the meeting analysis workflow.
- View generated summaries.
- Explore extracted action items and deadlines.
- Review generated follow-up emails.
- Download the email as a `.txt` file.
- Download the complete meeting analysis as a `.json` file.

---

## 🏗️ System Architecture

The application follows a sequential multi-agent architecture orchestrated using LangGraph.

Each agent performs a specialized task and contributes structured information to the shared workflow state.

### Workflow

```text
                Meeting Transcript
                        |
                        v
              +-------------------+
              |   Streamlit UI    |
              +-------------------+
                        |
                        v
              +-------------------+
              |  LangGraph State  |
              |    Management     |
              +-------------------+
                        |
                        v
              +-------------------+
              |  Summarization    |
              |      Agent        |
              +-------------------+
                        |
                        v
              +-------------------+
              |  Task Extraction  |
              |      Agent        |
              +-------------------+
                        |
                        v
              +-------------------+
              | Deadline Detection|
              |      Agent        |
              +-------------------+
                        |
                        v
              +-------------------+
              |  Email Generation |
              |      Agent        |
              +-------------------+
                        |
                        v
              +-------------------+
              | Structured Output |
              +-------------------+
                        |
                        v
              +-------------------+
              | Streamlit Results |
              |     Dashboard     |
              +-------------------+
                        |
                        v
             JSON / Email Downloads
```

### Agent Responsibilities

| Agent | Responsibility | Output |
|---|---|---|
| Summarization Agent | Summarizes the meeting and identifies key points and decisions | `MeetingSummary` |
| Task Extraction Agent | Extracts tasks, owners, and initial statuses | `TaskExtraction` |
| Deadline Detection Agent | Identifies deadlines and associated responsibilities | `DeadlineExtraction` |
| Email Generation Agent | Generates a follow-up email using the transcript and extracted information | `FollowUpEmail` |

### LangGraph Orchestration

LangGraph manages the workflow through a shared `MeetingState` object.

The workflow is implemented using the following nodes:

1. `summarize`
2. `extract_tasks`
3. `detect_deadlines`
4. `generate_email`

Each node processes the meeting information and updates the shared state with its corresponding structured output.

The graph executes sequentially, ensuring that the email generation agent receives the outputs produced by the earlier agents.

---

## 🧠 Technical Implementation

### State Management

The application uses a shared state structure defined through Python's `TypedDict`.

The state maintains:

- Original meeting transcript.
- Generated meeting summary.
- Extracted action items.
- Detected deadlines.
- Generated follow-up email.

This allows information to flow consistently between specialized agents.

### Structured Output Generation

The project uses **Pydantic** to define structured output schemas.

The schemas ensure that generated results follow predefined formats.

Implemented schemas include:

- `MeetingSummary`
- `ActionItem`
- `TaskExtraction`
- `DeadlineItem`
- `DeadlineExtraction`
- `FollowUpEmail`

The agents use LangChain's structured output functionality to generate responses conforming to these schemas.

### Prompt Engineering

Each specialized agent uses a dedicated system prompt.

The prompts are designed to:

- Extract only information supported by the transcript.
- Avoid inventing task owners or responsibilities.
- Distinguish suggestions from confirmed decisions.
- Preserve ambiguous deadline references.
- Generate concise and professional communication.

This helps improve consistency and reduce unsupported information in generated outputs.

---

## 📊 Evaluation Framework

The project includes an evaluation pipeline implemented in `evaluate.py`.

The evaluation script tests the system across **12 predefined meeting transcript scenarios** covering different meeting situations.

These scenarios include:

- Meetings with clearly assigned action items.
- Meetings with multiple responsible individuals.
- Meetings containing explicit deadlines.
- Meetings with ambiguous time references.
- Meetings without assigned tasks or confirmed deadlines.
- Discussions involving decisions and postponed activities.

### Evaluation Methodology

An independent LLM-based evaluator assesses the generated outputs against the original meeting transcripts.

The system is evaluated across four dimensions:

| Metric | Description |
|---|---|
| Summary Relevance | Measures how accurately the generated summary represents the meeting |
| Action Item Accuracy | Evaluates the correctness of extracted tasks and responsibilities |
| Deadline Accuracy | Measures the accuracy of detected deadlines |
| Faithfulness | Evaluates whether the generated output remains consistent with the original transcript |

Each dimension receives a score between **1 and 5**.

The evaluation script calculates an average score for every successfully evaluated scenario and saves the results to `evaluation_results.csv`.

**Note:** The repository contains the evaluation framework and predefined test scenarios. Actual benchmark scores should be reported only after running the evaluation script successfully.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| LLM | OpenAI GPT-4o-mini |
| Agent Orchestration | LangGraph |
| LLM Integration | LangChain |
| Structured Outputs | Pydantic |
| User Interface | Streamlit |
| Evaluation | LLM-as-a-Judge |
| Data Processing | Pandas |
| Configuration | Python-dotenv |

---

## 📂 Project Structure

```text
Meeting-Intelligence-System/
│
├── main.py                 # Streamlit application and user interface
├── graph.py                # LangGraph workflow and shared state management
├── agents.py               # Specialized AI agents and LLM integration
├── prompts.py              # System prompts for individual agents
├── schemas.py              # Pydantic models for structured outputs
├── evaluate.py             # Evaluation pipeline and test scenarios
├── requirements.txt        # Project dependencies
├── .env.example             # Environment variable template
├── .gitignore               # Files excluded from version control
└── README.md                # Project documentation
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/rithik2812/Meeting-Intelligence-System.git

cd Meeting-Intelligence-System
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory.

Use the `.env.example` file as a reference.

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

Replace the placeholder with your valid OpenAI API key.

**Important:** Never commit your actual API key or `.env` file to GitHub.

### 5. Run the Application

```bash
streamlit run main.py
```

The Streamlit application will start locally. Open the URL displayed in your terminal to access the dashboard.

---

## 🖥️ Application Workflow

### Step 1: Enter Meeting Transcript

Provide an unstructured meeting transcript through the Streamlit text input area.

### Step 2: Analyze Meeting

Click the **Analyze Meeting** button to initiate the multi-agent workflow.

### Step 3: Review Generated Insights

The application displays the generated information across four tabs:

- **Summary:** Meeting title, summary, key discussion points, and decisions.
- **Action Items:** Extracted tasks, owners, and statuses.
- **Deadlines:** Detected deadlines, associated tasks, and confidence levels.
- **Follow-up Email:** Generated email subject and body.

### Step 4: Download Results

Download the generated follow-up email as a text file or export the complete analysis as JSON.

---

## 🔐 Environment Variables

| Variable | Description | Default |
|---|---|---|
| `OPENAI_API_KEY` | API key used to access OpenAI models | Required |
| `OPENAI_MODEL` | OpenAI model used by the agents | `gpt-4o-mini` |

---

## ⚠️ Limitations

- The quality of generated insights depends on the completeness and clarity of the meeting transcript.
- Ambiguous speaker references and incomplete conversations may affect task ownership extraction.
- Relative deadline references are preserved as mentioned in the transcript and are not automatically converted into calendar dates.
- LLM-generated outputs may contain errors and should be reviewed before being used for official communication.
- The evaluation framework uses an LLM-based judge, so its scores are not equivalent to independently verified ground-truth benchmark metrics.
- The current implementation uses a sequential workflow rather than parallel agent execution.

---

## 🔮 Future Improvements

Potential extensions to the system include:

- Integration with audio transcription systems for direct meeting audio processing.
- Speaker identification and diarization.
- Calendar integration for deadline tracking and reminders.
- Persistent meeting history and searchable meeting records.
- Human feedback mechanisms for correcting extracted tasks and deadlines.
- Parallel execution of independent agents.
- More comprehensive evaluation using manually annotated ground-truth datasets.
- Integration with collaboration platforms such as Slack and Microsoft Teams.

---

## 👨‍💻 Author

**Rithik Anand**

B.Tech – Electrical and Electronics Engineering  
National Institute of Technology, Tiruchirappalli

**GitHub:** [rithik2812](https://github.com/rithik2812)

**Project Repository:** [AI-Powered Meeting Intelligence System](https://github.com/rithik2812/Meeting-Intelligence-System)

---

## 📄 License

This project is intended for academic and educational purposes.
