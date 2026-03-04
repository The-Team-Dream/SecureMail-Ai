from langgraph.graph import StateGraph, END
from app.core.state import AgentState
from app.agent.supervisor import supervising_agent_route
from app.agent.reviewer import reviewer_node
from app.agent.network_agent import network_node

#from app.core.scehmas import Techincal_Verdict

# Initialize the StateGraph with the AgentState
workflow = StateGraph(AgentState)

# Add nodes to the workflow
workflow.add_node("supervisor", supervising_agent_route)
workflow.add_node("reviewer", reviewer_node)
workflow.add_node("network_agent", network_node)

# Set the entry point for the workflow
workflow.set_entry_point("supervisor")

def get_next_node(state: AgentState) -> str:
    """Determine the next node based on the current state."""
    next_step = state.get("next")
    return "reviewer" if next_step == "FINISH" else next_step

def check_reviewer(state: AgentState) -> str:
    """Check the reviewer's state and determine the next action."""
    messages = state["messages"][-1].content
    last_message = messages[-1] if isinstance(messages, list) else messages
    content = last_message.content if hasattr(last_message, "content") else str(last_message)
    current_loop_count = state.get("loop_count", 0)

    if "REJECT" in content and current_loop_count < 1:
        return "LOOP"
    # Uncomment the following line if you want to return "FINISH" in other cases
    return END

# Define conditional edges for the workflow
workflow.add_conditional_edges("supervisor", get_next_node, {
    "network_agent": "network_agent",
    "reviewer": "reviewer"
})

# Add an edge to loop back to the supervisor
workflow.add_edge("network_agent", "supervisor")

# Add conditional edges for the reviewer


def update_loop_count(state: AgentState) -> dict:
    """Update the loop count in the state."""
    return {"loop_count": 1}

# Add a node to manage loops
workflow.add_node("LOOP_MANAGER", update_loop_count)
workflow.add_edge("LOOP_MANAGER", "supervisor")

# Add conditional edges for the reviewer to loop manager
workflow.add_conditional_edges(
    "reviewer",
    check_reviewer,
    {
        
        "LOOP_MANAGER": "LOOP_MANAGER",
        END: END,
    }
)

# Compile the workflow
app = workflow.compile()