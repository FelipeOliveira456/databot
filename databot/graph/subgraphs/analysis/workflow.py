from langgraph.graph import StateGraph, START, END
from databot.schemas.schemas import DataAnalysisState as State
from databot.graph.subgraphs.analysis.nodes import (
    generate_summary_node,
    generate_graphics_node,
    graphs_tool_node,
    analyze_plots_node,
    filter_useful_plots_node,
    generate_pdf_report_node,
    decision_plots_node
)

def create_analysis_graph():
    graph = StateGraph(State)

    graph.add_node("generate_summary", generate_summary_node)
    graph.add_node("decide_graphics", decision_plots_node)
    graph.add_node("generate_code", generate_graphics_node)
    graph.add_node("generate_plots", graphs_tool_node)
    graph.add_node("filter_plots", filter_useful_plots_node)
    graph.add_node("analyze_plots", analyze_plots_node)
    graph.add_node("generate_pdf", generate_pdf_report_node)

    graph.add_edge(START, "generate_summary")
    graph.add_edge("generate_summary", "decide_graphics")
    graph.add_edge("decide_graphics", "generate_code")
    graph.add_edge("generate_code", "generate_plots")
    graph.add_edge("generate_plots", "filter_plots")
    graph.add_edge("filter_plots", "analyze_plots")
    graph.add_edge("analyze_plots", "generate_pdf")
    graph.add_edge("generate_pdf", END)

    app = graph.compile()
    return app
