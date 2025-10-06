from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence
from langchain_ollama import ChatOllama
    
def get_query_gen() -> RunnableSequence:
    query_gen_template = """

    Você é um agente responsável por gerar consultas SQL para um banco de dados MySQL.

    Sua tarefa é:
    1. Traduzir a pergunta do usuário, escrita em linguagem natural, para uma consulta SQL válida.
    2. Retornar exclusivamente a **consulta SQL gerada**, sem explicações, comentários ou interpretações adicionais.

    ### Esquema do banco de dados:
    {schema}

    ### Pergunta:
    {question}

    ### Mensagens de erro anteriores (caso existam):
    {errors}

    Regras importantes:
    - A resposta ao usuário deve conter apenas a **consulta SQL**. Nada além disso.
    - Não inclua a cláusula LIMIT, a menos que o usuário solicite explicitamente.
    - Não utilize SELECT * — selecione apenas as colunas relevantes à pergunta.
    - Nunca utilize SUM() em colunas como "id", "codigo", "pedido", ou qualquer identificador único — isso é incorreto. Use COUNT() para contar registros.
    - Nunca produza comandos que modifiquem o banco de dados (como INSERT, UPDATE, DELETE, DROP, etc).
    - Caso a consulta contenha erros, ela será retornada a você. Sua tarefa será corrigi-la com base no erro informado.
    - Sempre formate a consulta SQL dentro de um bloco de código Markdown com a tag ```sql```.
    """

    query_gen_prompt = ChatPromptTemplate.from_template(query_gen_template)

    query_gen = query_gen_prompt | ChatOllama(
        model="qwen3-coder:30b",
        temperature=0.7,
        top_p=0.8,
        top_k=20,
    )

    return query_gen

