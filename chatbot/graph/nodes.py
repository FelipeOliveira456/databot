from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    RemoveMessage
)
from chatbot.agents.chatbot import (
    get_supervisor_agent,
    get_summarization_agent
)
from chatbot.schemas.schemas import ( 
    BaseState as State
)
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt

supervisor_agent = get_supervisor_agent()
summarization_agent = get_summarization_agent()

def supervisor_node(state: State):
    summary = state.get("summary", "")

    if summary:
        
        system_message = f"Summary of conversation earlier: {summary}"

        messages = [SystemMessage(content=system_message)] + state["messages"]
    
    else:
        messages = state["messages"]
    
    response = supervisor_agent.invoke(messages)
    
    return {"messages": response}

def summarization_node(state: State):
    # summary = state.get("summary", "")

    # if summary:
        
    #     summary_message = (
    #         f"This is summary of the conversation to date: {summary}\n\n"
    #         "Extend the summary by taking into account the new messages above:"
    #     )
    
    # else:
    #     summary_message = "Create a summary of the conversation above:"
    
    # messages = state["messages"] + [HumanMessage(content=summary_message)]
    # response = summarization_agent.invoke(messages)
    # delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-5]]
    # return {"summary": response.content, "messages": delete_messages}
    return {"messages": "rubinho"}

def human_node(state: State):
    to_user = state["messages"][-1]
    response = interrupt(to_user)
    message = HumanMessage(response)
    return {"messages": message}
