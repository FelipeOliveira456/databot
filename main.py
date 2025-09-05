from chatbot.graph.workflow import create_chatbot_graph
from chatbot.graph.subgraphs.sql.workflow import create_sql_graph
from chatbot.graph.subgraphs.analysis.workflow import create_analysis_graph
from pprint import pprint
import contextlib
import pandas as pd
from chatbot.schemas.schemas import DataAnalysisState
from chatbot.sql.connection import get_db

app = create_chatbot_graph()

questions = [
    "Quantas vendas foram realizadas em cada mês de cada ano?",                 # 1) Venda mensal acumulada
    "Quantas vendas foram registradas em cada ano?",                            # 2) Venda anual
    "Quantas vendas ocorreram em cada dia da semana?",                          # 3) Venda por dia da semana
    "Quantas vendas foram feitas em cada hora do dia?",                         # 4) Venda por hora
    "Como evoluiu a quantidade de vendas mês a mês em 2024, em termos percentuais?", # 5) Evolução dos meses
    "Quantas vendas foram feitas por grupo de produtos?",                       # 6) Venda por grupo de produtos
    "Quantas vendas foram feitas por produto individual?",                      # 7) Venda por produtos
    "Quantas vendas foram realizadas por forma de pagamento?",                  # 8) Venda por forma de recebimento
    "Quantas vendas foram atribuídas a cada cliente?",                          # 9) Venda por clientes
    "Quantas vendas foram feitas por segmento de clientes?",                    #10) Venda por segmento dos clientes
    "Quantas vendas foram realizadas por cada marketplace? A resposta deve associar o nome do marketplace com o numero de vendas", #11) Venda por marketplace
    "Quantas vendas foram atribuídas a cada vendedor?",                          #12) Venda por vendedor
    "Quantas vendas foram feitas por canal de venda?",                           #13) Venda por canal de venda
    "Quantas vendas foram realizadas em cada estado?"                            #14) Venda por estado
]

# Loop para invocar o app para cada pergunta
for i, question in enumerate(questions, 1):
    app.invoke({"input": question})

# for n in range(1, 6):
#     filename = f"test{n}.txt"
#     with open(filename, "w", encoding="utf-8") as f, contextlib.redirect_stdout(f):
#         for i, pergunta in enumerate(questions, start=1):
#             eventos = list(app.stream({"messages": [{"role": "user", "content": pergunta}]}, config={"recursion_limit": 50}, stream_mode="values"))
            
#             print(f"=== Pergunta {i} ===")
#             if len(eventos) >= 3:
#                 query_msg = eventos[-1]["messages"][-1].content
#                 print(query_msg)
#             else:
#                 print("Não há mensagens suficientes para capturar a query.")
#             print(f"=== Fim da resposta {i} ===\n")

question = """faça uma analise de dados sobre a seguinte questao: Quantas vendas foram realizadas em cada estado?
"""
reponse = app.invoke({"input": question})
