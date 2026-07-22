from langgraph.graph import StateGraph, END
from agents import (
    AgentState,
    hr_agent,
    skill_matching_agent,
    finance_agent,
    legal_agent,
    data_mining_agent,
    coordinator_agent,
)

workflow = StateGraph(AgentState)

workflow.add_node("hr_agent", hr_agent)
workflow.add_node("skill_matching_agent", skill_matching_agent)
workflow.add_node("finance_agent", finance_agent)
workflow.add_node("legal_agent", legal_agent)
workflow.add_node("data_mining_agent", data_mining_agent)
workflow.add_node("coordinator_agent", coordinator_agent)

workflow.set_entry_point("hr_agent")
workflow.add_edge("hr_agent", "skill_matching_agent")
workflow.add_edge("skill_matching_agent", "finance_agent")
workflow.add_edge("finance_agent", "legal_agent")
workflow.add_edge("legal_agent", "data_mining_agent")
workflow.add_edge("data_mining_agent", "coordinator_agent")
workflow.add_edge("coordinator_agent", END)

recruitment_app = workflow.compile()
