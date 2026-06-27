from langgraph.graph import StateGraph, END
from app.rag.agent_state import AgentState
from app.rag.agents import intent_agent, knowledge_agent, resolution_agent

def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("intent_agent", intent_agent)
    workflow.add_node("knowledge_agent", knowledge_agent)
    workflow.add_node("resolution_agent", resolution_agent)

    workflow.set_entry_point("intent_agent")
    workflow.add_edge("intent_agent", "knowledge_agent")
    workflow.add_edge("knowledge_agent", "resolution_agent")
    workflow.add_edge("resolution_agent", END)

    return workflow.compile()

if __name__ == "__main__":
    graph = build_graph()
    result = graph.invoke({"query": "How do I get a refund?"})
    print(f"\nFinal Answer: {result['answer']}")