from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import (
    ChatOllama,
)
from langchain_core.runnables import Runnable

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_core.messages import SystemMessage, HumanMessage

from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableSequence

def get_plot_decision_agent() -> RunnableSequence:
    plot_decision_template = """
    Você é um especialista em análise de dados e visualização. 
    Seu objetivo é **decidir quais gráficos gerar** para explorar os dados com base na solicitação do usuário e no resumo da análise exploratória (EDA).

    ### Entrada:
    - Pedido do usuário:  
    {user_request}

    - Resumo da análise exploratória:  
    {eda_summary}

    ### Regras gerais para decidir os gráficos:
    1. A seguir, diferentes categorias de gráficos:
    - **Distribuição**: gráficos que mostram a distribuição de uma única variável (ex: histograma, boxplot, densidade).
    - **Comparação entre categorias**: gráficos que comparam grupos/categorias (ex: barras, boxplots por grupo).
    - **Correlação / Relação**: gráficos que mostram relação entre variáveis (ex: dispersão, matriz de correlação).
    - **Séries temporais**: gráficos que mostram evolução ao longo do tempo (ex: linhas, área).
    - **Composição**: gráficos que mostram partes de um todo (ex: pizza, barras empilhadas).
    2. Evite gerar **mais de um gráfico da mesma classificação**, a não ser que a perspectiva seja muito diferente e necessária.
    3. Cada item da lista deve ser uma **descrição curta**, clara e objetiva, do tipo: "Gráfico de barras das vendas por categoria de produto".
    4. Se houver muitas categorias ou valores únicos, evite gráficos de fatias/pizza.
    5. Prefira gráficos que representem bem os dados sem excesso de ruído visual.
    6. Liste no máximo **5 gráficos por vez**.
    7. Retorne apenas **descrições de gráficos**, não gere código.

    ### Saída esperada:
    Retorne **um JSON válido** dentro de um bloco Markdown ```json```, contendo apenas uma lista de strings com as descrições dos gráficos escolhidos.

    ### Exemplo de saída:

    ```json
    [
    "Histograma da distribuição das idades dos clientes",
    "Gráfico de barras das vendas por categoria de produto",
    "Dispersão relacionando idade e salário",
    "Linha mostrando evolução das vendas ao longo do tempo"
    ]
    ```
    """

    plot_prompt = ChatPromptTemplate.from_template(plot_decision_template)

    plot_llm = ChatOllama(
        model="qwen3:32b",
        temperature=0.6,
        top_p=0.95,
        top_k=20,
    )

    return plot_prompt | plot_llm


def get_code_plot_agent() -> RunnableSequence:
    plot_decision_template = """
    Você é um especialista em geração de gráficos com Python para análise exploratória de dados (AED).

    Com base na lista de gráficos planejados, gere **uma lista de códigos Python**, onde cada código cria um gráfico diferente usando `matplotlib` e `seaborn`.

    ### Regras:
    - Cada código deve gerar um gráfico completo, começando com `plt.figure()`.
    - Não use `print()`, `plt.savefig()` ou `plt.close()`.
    - Use apenas as bibliotecas: matplotlib, seaborn, pandas, numpy.
    - Os dados já estão disponíveis em um DataFrame chamado `df`.
    - É permitido modificar `df` dentro do código (ex.: cópias, agregações, amostragens).

    - Gráficos planejados:  
    {planned_plots}

    - Colunas disponíveis:
    {column_metadata}

    ### Saída esperada:
    Retorne **apenas um JSON válido** dentro de um bloco Markdown ```json```, contendo uma lista de objetos com as chaves:
    - `"code"`: string com o código Python do gráfico.
    - `"description"`: breve descrição em **português**.

    Exemplo de saída:

    ```json
    [
    {{
        "code": "plt.figure()\\nsns.histplot(df['idade'], bins=30)\\nplt.title('Histograma da idade')",
        "description": "Histograma da distribuição da idade"
    }},
    {{
        "code": "plt.figure()\\nsns.boxplot(data=df, x='sexo', y='nota')\\nplt.title('Boxplot da nota por sexo')",
        "description": "Boxplot comparando notas entre os sexos"
    }}
    ]
    ```
    """

    plot_prompt = ChatPromptTemplate.from_template(plot_decision_template)

    plot_llm = ChatOllama(
        model="qwen3-coder:30b",
        temperature=0.7,
        top_p=0.8,
        top_k=20,
        repeat_penalty=1.05
    )

    return plot_prompt | plot_llm

def get_code_fix_agent() -> RunnableSequence:
    code_fix_template = """
    Você é um especialista em correção de código Python para geração de gráficos com matplotlib e seaborn.

    Você receberá:
    - Um código Python que tenta gerar um gráfico (variável `df` já disponível).
    - Uma mensagem de erro obtida ao executar esse código.

    Sua tarefa:
    - Corrigir o código para que ele funcione sem erros.
    - Manter a mesma intenção e o mesmo tipo de gráfico do código original.
    - Pode ajustar parâmetros, sintaxe, nomes de colunas, etc., para corrigir o problema.
    - Se necessário, criar variáveis auxiliares ou adaptar dados, mas nunca remover a essência do gráfico.
    - Use apenas as bibliotecas: matplotlib, seaborn, pandas, numpy.
    - Não inclua `plt.savefig()` ou `plt.close()`.
    - Não imprima nada no console.

    Entrada:
    ### Código original:
    {original_code}

    ### Erro:
    {error_message}

    ### Colunas disponíveis:
    {column_metadata}

    Saída esperada:
    Retorne apenas o código Python corrigido, pronto para execução, dentro de um bloco Markdown ```python```.
    Não inclua explicações, comentários ou texto fora do bloco de código.
    """

    fix_prompt = ChatPromptTemplate.from_template(code_fix_template)

    fix_llm = ChatOllama(
        model="qwen3-coder:30b",
        temperature=0.7,
        top_p=0.8,
        top_k=20,
        repeat_penalty=1.05
    )

    return fix_prompt | fix_llm


def get_visual_analysis_agent() -> Runnable:
    system_prompt = """
    Você é um especialista em interpretação de gráficos.

    Dada uma imagem de gráfico enviada pelo usuário, forneça uma análise clara e detalhada sobre o que o gráfico mostra, em no máximo 5 linhas.

    Descreva em PORTUGUES:
    - O tipo de gráfico.
    - As variáveis envolvidas (nomes, eixos, categorias, etc.).
    - Tendências, padrões, outliers ou insights importantes que ele revela.

    Seja objetivo e informativo, como se estivesse explicando para alguém que não tem o gráfico em mãos.    
    """

    def prompt_func(data):
      text = data["text"]
      image = data["image"]

      image_part = {
          "type": "image_url",
          "image_url": f"data:image/png;base64,{image}",
      }

      content_parts = []

      text_part = {"type": "text", "text": text}

      content_parts.append(image_part)
      content_parts.append(text_part)

      return [SystemMessage(system_prompt), HumanMessage(content=content_parts)]

    llm = ChatOllama(
        model="qwen2.5vl:32b",
        temperature=0.3,
        top_p=0.9,
        top_k=20,
        repeat_penalty=1.05
    )

    return prompt_func | llm 

def get_visual_quality_agent() -> Runnable:
    system_prompt = """
    Você é um avaliador de qualidade de gráficos.

    Sua tarefa é analisar a imagem de um gráfico enviada pelo usuário e responder APENAS com
    um número decimal entre 0 e 1, indicando a qualidade do gráfico:
    - 0 significa um gráfico péssimo (ilegível, confuso, irrelevante).
    - 1 significa um gráfico excelente (claro, informativo, bem apresentado).

    Diretrizes para avaliar a qualidade:
    - As legendas, títulos e rótulos de eixos devem ser legíveis e claros.
    - As cores ou formas devem diferenciar bem as categorias ou valores.
    - O tipo de gráfico deve ser adequado ao tipo de dado.
    - Não deve haver poluição visual, excesso de elementos ou confusão.
    - Os dados devem ser apresentados de forma que facilite a interpretação e extração de insights.

    Não adicione explicações, texto, palavras ou símbolos, apenas o número decimal entre 0 e 1.
    """

    def prompt_func(data):
          text = data["text"]
          image = data["image"]

          image_part = {
              "type": "image_url",
              "image_url": f"data:image/png;base64,{image}",
          }

          content_parts = []

          text_part = {"type": "text", "text": text}

          content_parts.append(image_part)
          content_parts.append(text_part)

          return [SystemMessage(system_prompt), HumanMessage(content=content_parts)]

    llm = ChatOllama(
        model="qwen2.5vl:32b",
        temperature=0.3,
        top_p=0.9,
        top_k=20,
        repeat_penalty=1.05
    )

    return prompt_func | llm

def get_pdf_report_agent() -> RunnableSequence:
    report_template = """
    Você é um assistente especializado em análise exploratória de dados e criação de relatórios em Markdown.

    Você receberá:
    - Estatísticas descritivas de um conjunto de dados (mínimo, máximo, média, etc.). 
    - IMPORTANTE: **analise cuidadosamente os dados e inclua apenas o que for relevante**.  
    Não inclua informações óbvias ou triviais (por exemplo, "um dia tem 24 horas").
    - Lista de gráficos, cada um com:
    - Caminho do arquivo da imagem
    - Descrição do gráfico
    - Análise textual já feita para o gráfico
    - Diretriz do usuário sobre o que ele espera do relatório.

    Sua tarefa:
    - Criar um relatório em Markdown em PORTUGUÊS, claro, coeso e informativo.
    - Você pode:
    - Organizar as informações da forma que fizer mais sentido
    - Destacar **insights importantes** e padrões relevantes
    - Resumir estatísticas e análises
    - Incluir observações contextuais relevantes
    - **Não invente dados** que não foram passados.
    - Use somente o nome do arquivo para as imagens (ex.: `grafico.png`), pois elas estarão no diretório de imagens.

    Estrutura sugerida para o relatório:

    1. **Introdução**
    - Contextualize brevemente os dados e o objetivo da análise.
    - Explique de forma resumida o que o usuário solicitou.

    2. **Resumo Estatístico**
    - Apresente as estatísticas descritivas relevantes.
    - Destaque padrões, tendências ou valores extremos significativos.

    3. **Análise dos Gráficos**
    - Para cada gráfico:
        - Nome do arquivo da imagem
        - Descrição resumida do que o gráfico mostra
        - Insights principais com base na análise textual fornecida
        - Comentários adicionais se houver padrões ou relações importantes

    4. **Observações Gerais**
    - Pontos importantes que surgem da análise conjunta de estatísticas e gráficos
    - Tendências, correlações ou anomalias relevantes
    - Sugestões ou alertas contextuais

    5. **Conclusão**
    - Síntese dos principais insights
    - Implicações ou próximos passos sugeridos (sem inventar dados)
    - Destaque final dos padrões mais relevantes identificados

    Entrada:
    ### Diretriz do usuário:
    {user_input}

    ### Estatísticas descritivas:
    {stats}

    ### Gráficos:
    {plots}

    Saída esperada:
    Retorne o relatório **dentro de um bloco de código Markdown**:

    ```markdown
    (conteúdo do relatório aqui)
    ```
    """

    report_prompt = ChatPromptTemplate.from_template(report_template)

    report_llm = ChatOllama(
        model="qwen3:32b", 
        temperature=0.6,
        top_p=0.9,
        top_k=20,
    )

    return report_prompt | report_llm