from typing import TypedDict, Optional

class AgentState(TypedDict):
    query: str
    intent: Optional[str]
    context: Optional[str]
    answer: Optional[str]