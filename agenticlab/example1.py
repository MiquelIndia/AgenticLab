from typing import TypedDict, List
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    task: str
    plan: List[str]
    research: str
    output: str

def planner_agent(state: AgentState) -> AgentState:
    state["plan"] = [
        "Understand the task",
        "Research the topic",
        "Write a clear answer"
    ]
    return state

def research_agent(state: AgentState) -> AgentState:
    topic = state["task"]
    state["research"] = f"Key facts about {topic} (pretend this is researched)."
    return state

def writer_agent(state: AgentState) -> AgentState:
    state["output"] = (
        f"Task: {state['task']}\n\n"
        f"Plan:\n- " + "\n- ".join(state["plan"]) + "\n\n"
        f"Research:\n{state['research']}\n\n"
        f"Final Answer:\nThis is a well-written response."
    )
    return state

def build_graph() -> StateGraph:

    graph = StateGraph(AgentState)
    # Register agents
    graph.add_node("planner", planner_agent)
    graph.add_node("researcher", research_agent)
    graph.add_node("writer", writer_agent)

    # Define execution flow
    graph.set_entry_point("planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", END)

    app = graph.compile()
    return app


def main():
    print("Hello, AgenticLab!")
    app = build_graph()
    initial_state = {
        "task": "Explain multi-agent systems in simple terms",
        "plan": [],
        "research": "",
        "output": ""
    }

    final_state = app.invoke(initial_state)

    print(final_state["output"])


if __name__ == "__main__":
    main()