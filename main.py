from crewai import LLM
from crewai import Agent, Task, Crew, Process
from pathlib import Path

# -----------------------------
# Load framework context
# -----------------------------

def load_file(path):
    return Path(path).read_text()

framework = load_file("agents/product_owner/agent_framework.md")
notes = load_file("NOTES.md")

# -----------------------------
# Input (simulation mode)
# -----------------------------

print("\n=== Product Owner Agent Simulation Runner ===\n")
stakeholder_input = input("Enter stakeholder request:\n> ")

# -----------------------------
# Define Agent
# -----------------------------

llm = LLM(
    model="gpt-4o-mini"
)

po_agent = Agent(
    role="Product Owner Agent",
    goal="Analyze stakeholder input, clarify ambiguity, identify risks/dependencies, and produce refinement-ready stories.",
    backstory=framework,
    verbose=True,
    llm=llm
)

# -----------------------------
# Define Task
# -----------------------------

task = Task(
    description=f"""
You are a Product Owner Agent.

Analyze the stakeholder input using your framework.

Stakeholder input:
{stakeholder_input}

Follow your internal rules for:
- ambiguity handling
- clarification
- risk identification
- dependency detection
- story decomposition (only if appropriate)

Do NOT repeat the framework back.
Do NOT output raw context files.
Focus on reasoning and structured PO output.
""",
    expected_output="Refinement-ready PO analysis with clarification, risks, dependencies, and optional story breakdown.",
    agent=po_agent
)

# -----------------------------
# Run Crew
# -----------------------------

crew = Crew(
    agents=[po_agent],
    tasks=[task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()

print("\n\n===== PO AGENT OUTPUT =====\n")
print(result)

