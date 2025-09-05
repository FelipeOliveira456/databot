from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from chatbot.tools.chatbot import RouteSupervisor

# def get_supervisor_agent():
#     system_prompt = """
#     Você é um agente supervisor responsável por orquestrar uma cadeia de subgrafos, cada um com uma função específica.

#     Seu trabalho é, a cada etapa, **decidir qual subgrafo deve ser chamado a seguir** com base nas mensagens trocadas até o momento, na saída da etapa anterior, na task atual e no resumo.

#     O estado contém:
#     - task atual: {task}  # contém "subgraph" e "description"
#     - caminho do CSV (pode estar vazio se nenhum CSV foi gerado): {csv_path}

#     Os subgrafos disponíveis são:
#     - "sql": para geração de consultas SQL a partir da task atual.
#     - "analysis": para interpretações e análises com base nos dados obtidos pela query SQL.

#     ### Regras:
#     - Nunca chame "analysis" antes de uma task "sql" concluída.
#     - Se a query SQL já foi gerada e os dados salvos em CSV, não retorne mais para "sql".
#     - Somente quando todas as tasks forem concluídas, retorne a mensagem final diretamente ao usuário.

#     ### Mensagens anteriores:
#     {messages}

#     ### Resumo:
#     {resume}
#     """

#     summarization_prompt = ChatPromptTemplate.from_template(system_prompt)

#     supervisor_agent = summarization_prompt | ChatOllama(
#         model="qwen3:32b",
#         temperature=0.3,
#         top_p=0.9,
#         top_k=50,
#     ).bind_tools([RouteSupervisor])

#     return supervisor_agent

# def get_summary_agent():
#     summary_template = """
#     Você é um agente responsável por criar e atualizar um resumo textual com base nas mensagens trocadas.

#     Você receberá:
#     - O resumo atual pode estar vazio.
#     - Uma nova mensagem deve ser incorporada ao resumo.

#     Sua tarefa é gerar um novo resumo atualizado que:

#     - Inclua as informações do resumo anterior mais a nova mensagem.
#     - Cresça no máximo 4 linhas a mais que o resumo anterior.
#     - Seja claro, objetivo e conciso.
#     - Caso o limite seja ultrapassado, faça um truncamento elegante para manter o tamanho.
#     - Na parte de análise, não seja específico sobre quais gráficos gerar, a não ser que o usuário peça de maneira explícita.
    
#     ### Dados recebidos:
#     Resumo atual:
#     {summary}

#     Nova mensagem:
#     {new_message}

#     Retorne **apenas** um JSON no seguinte formato:

#     ```json
#     {{
#       "summary": "Aqui vai o novo resumo atualizado, com até 4 linhas a mais que o anterior."
#     }}
#     ```
#     """

#     summary_prompt = ChatPromptTemplate.from_template(summary_template)

#     summary_llm = ChatOllama(
#         model="qwen3:32b",
#         temperature=0.3,
#         top_p=0.9,
#         top_k=40,
#     )

#     return summary_prompt | summary_llm

def get_task_agent():
    task_decision_template = """
    Você é um agente especializado em planejamento de tarefas para um pipeline de análise de dados.

    Sua função é transformar a mensagem do usuário em uma lista de **tarefas claras e sequenciais**,
    onde cada tarefa indica explicitamente qual **subgrafo** deve ser usado.

    ### Subgrafos disponíveis:
    - "sql": para geração de consultas SQL a partir da solicitação.
    - "analysis": para interpretações, análises ou geração de gráficos com base nos dados obtidos via SQL ou arquivos fornecidos (como CSV).
    - "END": para encerrar quando o pedido do usuário for vago, ambíguo ou não for possível determinar os passos.

    ### Regras:
    - Sempre retorne em formato **JSON válido** dentro de um bloco Markdown com ```json```.
    - O JSON deve ter a forma:
    ```json
    {{
      "tasks": [
        {{
          "subgraph": "sql" ou "analysis" ou "END",
          "description": "descrição curta do que deve ser feito nesta etapa"
        }}
      ]
    }}
    ```
    - É permitido que todas as tarefas sejam apenas de "sql", caso o pedido do usuário seja apenas de recuperação de dados.
    - É permitido que todas as tarefas sejam apenas de "analysis", caso o usuário forneça diretamente um arquivo (como CSV) ou apenas queira uma análise sem consulta a banco.
    - Nunca use o subgrafo "analysis" antes de pelo menos uma tarefa de "sql", exceto se os dados já forem fornecidos pelo usuário (ex.: CSV).
    - Se a tarefa for de "analysis", não seja específico sobre o tipo de gráfico a ser gerado, pois o subgrafo já se encarrega da escolha apropriada. Seja explícito sobre o tipo de gráfico apenas se o usuário mencionar algum tipo específico na solicitação.    
    - Se o pedido for vago, ambíguo ou não compreensível, retorne diretamente "subgraph": "END" com uma descrição pedindo exclarecimentos.
    - Cada descrição deve ser curta, direta e começar com um verbo no infinitivo.
    - Liste as tarefas em ordem lógica de execução.

    ### Exemplos de saída:

    #### Caso apenas SQL seja necessário:
    ```json
    {{
      "tasks": [
        {{
          "subgraph": "sql",
          "description": "Gerar a query SQL para listar todos os clientes ativos"
        }}
      ]
    }}
    ```

    #### Caso SQL + Analysis sejam necessários:
    ```json
    {{
      "tasks": [
        {{
          "subgraph": "sql",
          "description": "Gerar a query SQL para recuperar as vendas do último mês"
        }},
        {{
          "subgraph": "analysis",
          "description": "Analisar as tendências de vendas por categoria de produto"
        }}
      ]
    }}
    ```

    #### Caso o usuário forneça CSV diretamente:
    ```json
    {{
      "tasks": [
        {{
          "subgraph": "analysis",
          "description": "Analisar os dados de vendas por Marketplace"
        }} 
      ]
    }}
    ```

    #### Caso o pedido seja vago/ambíguo:
    ```json
    {{ 
      "tasks": [
        {{
          "subgraph": "END",
          "description": "Encerrar pois o pedido do usuário é vago ou ambíguo"
        }}
      ]
    }}
    ```

    ### Entrada:
    - Mensagem do usuário:  
    {user_message}

    - Caminho do arquivo CSV (se houver):  
    {user_csv}
    """

    task_prompt = ChatPromptTemplate.from_template(task_decision_template)

    task_llm = ChatOllama(
        model="qwen3:32b",
        temperature=0.6,
        top_p=0.95,
        top_k=20,
    )

    return task_prompt | task_llm
