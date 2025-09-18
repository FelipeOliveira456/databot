from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

def get_task_evaluator_agent_simple():
    task_evaluator_template = """
    Você é um agente especializado em **avaliar tarefas de análise de dados**.

    Sua função é comparar duas listas de tarefas:
    1. A lista correta de tasks (`gold_tasks`).
    2. A lista predita pelo sistema (`predicted_tasks`).

    Cada task tem:
    - `subgraph`: "sql", "analysis", ou "END"
    - `description`: uma descrição curta da tarefa

    ### Objetivo:
    - Avaliar se as descrições das tasks preditas **fazem sentido e estão coerentes com o objetivo geral** das tasks corretas.
    - Ignore quantidade, posição ou ordem das tarefas — avalie apenas se as descrições são relevantes e fazem sentido no contexto.

    ### Escala de notas:
    - **0 a 3** → Descrições sem sentido, aleatórias ou irrelevantes
    - **4 a 6** → Algumas descrições fazem sentido, mas várias estão confusas ou pouco relacionadas
    - **7 a 9** → A maioria das descrições faz sentido e está próxima do objetivo, com poucos desvios
    - **10** → Todas as descrições fazem sentido e estão claramente alinhadas ao objetivo

    ### Regras:
    - Retorne **apenas a nota como um número inteiro de 0 a 10**
    - Não inclua explicações, textos ou justificativas

    ### Entrada:
    - Lista de tasks correta:  
    {gold_tasks}

    - Lista de tasks predita:  
    {predicted_tasks}
    """

    evaluator_prompt = ChatPromptTemplate.from_template(task_evaluator_template)

    evaluator_llm = ChatOllama(
        model="gpt-oss:20b",
        temperature=1.0,
        top_p=0.95,
        top_k=20,
    )

    return evaluator_prompt | evaluator_llm
