from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.rag.graph import build_graph

router = APIRouter(prefix="/chat", tags=["Chat"])

graph = build_graph()

@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = graph.invoke({"query": request.message})
    return {
        "intent": result["intent"],
        "answer": result["answer"]
    }