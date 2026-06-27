from app.rag.agent_state import AgentState
from app.rag.vectorstore import get_vectorstore
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

# ---------- Intent Agent ----------
def intent_agent(state: AgentState) -> AgentState:
    query = state["query"]

    prompt = f"""Classify the customer's intent into ONE of these categories:
refund, login_issue, order_tracking, subscription, payment_issue, other

Customer message: {query}

Respond with ONLY the category name, nothing else."""

    response = llm.invoke(prompt)
    intent = response.content.strip().lower()

    state["intent"] = intent
    print(f"[Intent Agent] Detected intent: {intent}")
    return state

# ---------- Knowledge Agent ----------
def knowledge_agent(state: AgentState) -> AgentState:
    query = state["query"]
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search(query, k=3)
    context = "\n\n".join([doc.page_content for doc in results])

    state["context"] = context
    print(f"[Knowledge Agent] Retrieved context for intent: {state['intent']}")
    return state

# ---------- Resolution Agent ----------
def resolution_agent(state: AgentState) -> AgentState:
    query = state["query"]
    context = state["context"]

    prompt = f"""You are a customer support assistant. Answer the customer's question using ONLY the context below.
If the answer is not in the context, say "I don't have information about that, let me escalate this to a human agent."

Context:
{context}

Customer Question: {query}

Answer:"""

    response = llm.invoke(prompt)
    state["answer"] = response.content
    print(f"[Resolution Agent] Generated final answer")
    return state