from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from chatbot.tools.chatbot import RouteSupervisor

def get_supervisor_agent():

    system_prompt = """
    You are a supervisor tasked with managing a conversation between the following workers: sql.

    Your responsibilities are:
    1. Read the current conversation (provided as a list of messages).
    2. Decide which worker should handle the next step of the task.
        - If the task requires a subgraph like "sql", forward the task to the corresponding worker.
    3. Generate a message for the selected worker to continue the task, or respond directly to the user if no tool is needed.

    If the task should proceed to another worker (e.g., sql), use the tool to forward the message.
    If no action is needed (i.e., the message is for the user), **do not use the tool** and respond directly.

    Tools available:
    - sql: A tool to forward the task to the SQL worker. It should only be used if the task is to be delegated to an agent.
    """

    summarization_prompt = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("placeholder", "{messages}")])

    supervisor_agent = summarization_prompt | ChatOllama(model="teste", temperature=0).bind_tools(
        [RouteSupervisor]
    )
    return supervisor_agent

def get_summarization_agent():

    system_prompt = """
    You are a summarization agent.

    You will be given:
    - An existing summary of a conversation so far (may be empty)
    - A list of messages

    Your task is to update the summary by incorporating the most important new information from the messages. The updated summary should reflect the entire conversation up to this point.

    Guidelines:
    - Preserve relevant content from the existing summary
    - Integrate key points, decisions, or questions from the new messages
    - Keep the summary concise and focused
    - If the existing summary is empty, generate a new one from scratch
    - Do not repeat unchanged information
    - Ignore irrelevant or off-topic content

    Return only the updated summary as plain text.
    """

    summarization_prompt = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("placeholder", "{messages}")])

    summarization_gen = summarization_prompt | ChatOllama(model="gpt-4o", temperature=0)

    return summarization_gen


