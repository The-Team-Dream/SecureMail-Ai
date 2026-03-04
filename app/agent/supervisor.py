import os
from typing import Literal
from langchain_groq import ChatGroq 
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from pydantic import BaseModel
from app.core.state import AgentState
from app.core.config import GROQ_API_KEY, supervisor_model, WORK_Model


members=["network_agent"]

llm = ChatGroq(
    model=supervisor_model,
    temperature=0.0,          # ✅ تصحيح الإملاء
    api_key=GROQ_API_KEY      # ✅ استخدام الاسم الصحيح (api_key)
)

class RouteDecision(BaseModel):
    next: Literal["network_agent","FINISH"]



# app/agents/supervisor.py

system_prompt = (
    "You are a workflow router. Your goal is to move the task forward.\n"
    "\n"
    "STRICT ROUTING RULES (Follow in order):\n"
    "1. LOOK at the LAST message in the conversation.\n"
    "\n"
    "2. IF the last message is from 'network_agent' (it contains a report or verdict):\n"
    "   -> YOU MUST SELECT 'FINISH' immediately.\n"
    "   -> Do NOT send it back to network_agent.\n"
    "\n"
    "3. IF the last message contains 'REJECT' (from Reviewer):\n"
    "   -> SELECT 'network_agent' to fix the error.\n"
    "\n"
    "4. IF the last message is from the User (new investigation):\n"
    "   -> SELECT 'network_agent'.\n"
)
prompt=ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        ("human","given converstation above,who should I route to next? choose one from the following options: {members} or FINISH if the investigation is complete. Just answer with the option name without any explanation.")
    ]
).partial(members=",".join(members))

supervising_agent=prompt | llm.with_structured_output(RouteDecision)


def supervising_agent_route(state:AgentState):
    decission=supervising_agent.invoke(state)
    return{
        "next":decission.next
    }
