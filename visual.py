import argparse
from langchain_core.runnables.graph import MermaidDrawMethod
from databot.graph.workflow import create_databot_graph
from databot.graph.subgraphs.analysis.workflow import create_analysis_graph
from databot.graph.subgraphs.sql.workflow import create_sql_graph

def get_graph(name: str):
    graphs = {
        "databot": create_databot_graph,
        "analysis": create_analysis_graph,
        "sql": create_sql_graph,
    }
    if name not in graphs:
        raise ValueError(f"Grafo inválido: {name}. Use 'databot', 'analysis' ou 'sql'.")
    app = graphs[name]()
    return app.get_graph(xray=1)  

def generate_and_save_png(graph, output_file: str):
    graph_png = graph.draw_mermaid_png(draw_method=MermaidDrawMethod.PYPPETEER)
    with open(output_file, "wb") as f:
        f.write(graph_png)
    print(f"✅ Grafo gerado e salvo em formato PNG: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Salva grafo LangGraph como PNG.")
    parser.add_argument(
        "-g", "--graph",
        choices=["databot", "analysis", "sql"],
        default="databot",
        help="Nome do grafo a gerar (padrão: databot)"
    )
    
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Nome do arquivo de saída (ex: graph.png)"
    )
    
    args = parser.parse_args()

    graph = get_graph(args.graph)
    output_file = args.output or f"{args.graph}_graph.png"
    generate_and_save_png(graph, output_file)

if __name__ == "__main__":
    main()
