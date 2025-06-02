from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from chatbot.tools.chatbot import RouteSupervisor

def get_supervisor_agent():

    system_prompt = """
    Você é um supervisor encarregado de gerenciar uma conversa entre os seguintes trabalhadores: sql.

    Suas responsabilidades são:
    1. Ler a conversa atual (fornecida como uma lista de mensagens).
    2. Decidir qual trabalhador deve lidar com o próximo passo da tarefa.
    - Se a tarefa exigir um subgrafo como "sql", encaminhe a tarefa para o trabalhador correspondente.
    3. Gerar uma mensagem para o trabalhador selecionado continuar a tarefa, ou responder diretamente ao usuário se nenhuma ferramenta for necessária.

    Se a tarefa deve prosseguir para outro trabalhador (por exemplo, sql), use a ferramenta para encaminhar a mensagem.
    Se nenhuma ação for necessária (ou seja, a mensagem é para o usuário), **não use a ferramenta** e responda diretamente.

    Ferramentas disponíveis:
    - sql: Uma ferramenta para encaminhar a tarefa ao trabalhador SQL. Deve ser usada apenas se a tarefa for delegada a um agente.

    Use apenas as ferramentas listadas acima.
    """

    summarization_prompt = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("placeholder", "{messages}")])

    supervisor_agent = summarization_prompt | ChatOllama(model="qwen3:8b", temperature=0.2).bind_tools(
        [RouteSupervisor]
    )
    return supervisor_agent


