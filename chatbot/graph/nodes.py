from chatbot.agents.chatbot import (
    get_supervisor_agent,
)
from chatbot.schemas.schemas import ( 
    BaseState as State
)
from chatbot.graph.subgraphs.sql.workflow import create_sql_graph
from langchain_core.messages import AIMessage

supervisor_agent = get_supervisor_agent()
sql_graph = create_sql_graph()

def supervisor_node(state: State):
    response = supervisor_agent.invoke({"messages": state["messages"]})
    
    return {"messages": response}

def sql_node(state: State):

    last_message = state["messages"][-1]
    tool_call = last_message.tool_calls[-1]
    message = tool_call["args"]["message"]
    first_state = {"messages": message}

    result = sql_graph.invoke(first_state)
    response = result["messages"][-3]
    query = AIMessage(response.tool_calls[-1]["args"]["query"])
    return {"messages": query}

    