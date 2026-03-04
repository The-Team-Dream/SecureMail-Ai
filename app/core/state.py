import operator
from typing import Annotated, List, TypedDict
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    next: str
    # ✅ التصحيح هنا: لازم تستخدم Annotated وتفتح القوس بتاعها [ ]
    loop_count: Annotated[int, operator.add]