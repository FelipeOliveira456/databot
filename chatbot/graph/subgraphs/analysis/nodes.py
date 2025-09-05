from typing import cast
import pandas as pd
import io
from chatbot.schemas.schemas import (
    DataAnalysisState, 
    PlotWithAnalysis
)
from chatbot.tools.analysis import (
    execute_plot_code,
    generate_pdf_from_markdown
)
from chatbot.agents.analysis import (
    get_code_plot_agent,
    get_visual_analysis_agent,
    get_code_fix_agent,
    get_visual_quality_agent,
    get_pdf_report_agent,
    get_plot_decision_agent
)
from chatbot.graph.subgraphs.analysis.utils import (
    convert_to_base64,
    extract_python_code,
    format_plots_for_agent_plain,
    extract_markdown
)
import re
import json 

def generate_summary_node(state: DataAnalysisState) -> DataAnalysisState:
    df = cast(pd.DataFrame, state["df"])
    summary = []

    summary.append(f"O DataFrame contém {df.shape[0]} linhas e {df.shape[1]} colunas.\n")

    for col in df.columns:
        col_data = df[col]
        summary.append(f"Coluna '{col}':")
        summary.append(f"- Tipo: {col_data.dtype}")

        # Valores ausentes
        n_missing = col_data.isna().sum()
        pct_missing = (n_missing / len(col_data)) * 100
        summary.append(f"- Valores ausentes: {n_missing} ({pct_missing:.1f}%)")

        if pd.api.types.is_numeric_dtype(col_data):
            desc = col_data.describe()
            median = col_data.median()
            summary.append(f"- Estatísticas numéricas:")
            summary.append(f"  • Média: {desc['mean']:.2f}")
            summary.append(f"  • Mediana: {median:.2f}")
            summary.append(f"  • Desvio padrão: {desc['std']:.2f}")
            summary.append(f"  • Mínimo: {desc['min']:.2f}")
            summary.append(f"  • Máximo: {desc['max']:.2f}")
            summary.append(f"  • 25%: {desc['25%']:.2f}")
            summary.append(f"  • 50%: {desc['50%']:.2f}")
            summary.append(f"  • 75%: {desc['75%']:.2f}")

            n_unique = col_data.nunique()
            total = len(col_data)
            if n_unique <= 20 or n_unique / total < 0.05:
                summary.append(f"- Tipo numérico detectado: discreto (valores únicos: {n_unique})")
            else:
                summary.append(f"- Tipo numérico detectado: contínuo")

        else:
            desc = col_data.describe()
            summary.append(f"- Estatísticas categóricas:")
            summary.append(f"  • Valores únicos: {desc['unique']}")
            summary.append(f"  • Valor mais frequente: {desc['top']}")
            summary.append(f"  • Frequência do valor mais frequente: {desc['freq']}")

        summary.append("")  # linha em branco para separar colunas

    return {
        **state,
        "eda_summary": "\n".join(summary)
    }

decision_llm = get_plot_decision_agent()

def decision_plots_node(state: DataAnalysisState):
    """
    Node que decide quais gráficos gerar com base na solicitação do usuário e no EDA summary.
    Atualiza o estado com 'planned_plots': lista de descrições de gráficos.
    """
    user_request = state.get("input", "")
    eda_summary = state.get("eda_summary", "")

    response = decision_llm.invoke({
        "user_request": user_request,
        "eda_summary": eda_summary
    })

    match = re.search(r"```json\s*(.*?)\s*```", response.content, re.DOTALL | re.IGNORECASE)
    if match:
        json_str = match.group(1).strip()  
        planned_plots = json.loads(json_str)  
    else:
        planned_plots = ""

    planned_plots = json.loads(json_str)

    return {
        **state,
        "planned_plots": planned_plots
    }

code_llm = get_code_plot_agent()

def generate_graphics_node(state: DataAnalysisState) -> DataAnalysisState:
    planned_plots = state.get("planned_plots", "")
    planned_plots_str = "\n".join(planned_plots)
    df = state["df"]
    buffer = io.StringIO()
    df.info(buf=buffer)
    column_metadata = buffer.getvalue()

    response = code_llm.invoke({
        "planned_plots": planned_plots_str,
        "column_metadata": column_metadata
    })

    content = response.content

    match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL | re.IGNORECASE)
    if match:
        tool_calls = match.group(1).strip()
    else:
        tool_calls = ""
    
    return {
        **state,
        "tool_calls": tool_calls
    } 

code_fix_llm = get_code_fix_agent()

def graphs_tool_node(state: DataAnalysisState) -> DataAnalysisState:
    raw_tool_calls = state.get("tool_calls", "")
    print(raw_tool_calls)
    df = state["df"]
    buffer = io.StringIO()
    df.info(buf=buffer)
    column_metadata = buffer.getvalue()


    tool_calls = json.loads(raw_tool_calls)
    plots = []

    for call in tool_calls:
        code = call.get("code")
        description = call.get("description", "")

        try:
            result = execute_plot_code(df=df, code=code)
            plot: PlotWithAnalysis = {
                "path": result["path"],
                "description": description,
            }
            plots.append(plot)

        except Exception as e:
            print(e)
            error_msg = str(e)

            print("agente de correção de código")
            fix_response = code_fix_llm.invoke({
                "original_code": code,
                "error_message": error_msg,
                "column_metadata": column_metadata
            })

            fixed_code = extract_python_code(
                fix_response.content
            )

            if fixed_code.strip():
                try:
                    result = execute_plot_code(df=df, code=fixed_code)
                    plot: PlotWithAnalysis = {
                        "path": result["path"],
                        "description": description,
                    }
                    plots.append(plot)
                except Exception:
                    pass       

    return {
        **state,
        "plots": plots
    }

visual_llm = get_visual_analysis_agent()

def analyze_plots_node(state: DataAnalysisState) -> DataAnalysisState:
    plots = state.get("plots", [])
    for plot in plots:
        description = plot.get("description", "")
        path = plot.get("path")
        image_base64 = convert_to_base64(path)

        print("agente de analise visual")
        response = visual_llm.invoke({
            "text": description,
            "image": image_base64
        })
        content = response.content
        plot["analysis"] = content
        print(f"Descricao: {plot['description']}")
        print(f"Analise: {plot['analysis']}")
        print("---------------------------------------------")
    
    return {
        **state,
        "plots": plots,
    }

visual_quality_llm = get_visual_quality_agent()

def filter_useful_plots_node(state: DataAnalysisState) -> DataAnalysisState:
    plots = state.get("plots", [])
    filtered_plots = []

    for plot in plots:
        description = plot.get("description", "")
        path = plot.get("path")
        image_base64 = convert_to_base64(path)

        print("agente de filtrar imagens uteis")
        response = visual_quality_llm.invoke({
            "text": description,
            "image": image_base64
        })

        content = str(response.content).strip()
        print("Resposta do agente de qualidade:", content)

        score = 0.0
        try:
            # Extrair JSON dentro de bloco ```json ... ```
            match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL | re.IGNORECASE)
            if match:
                json_str = match.group(1).strip()
                data = json.loads(json_str)
                score = float(data.get("score", 0.0))
            else:
                print("Nenhum bloco JSON encontrado, usando score 0.0")
                score = 0.0
        except Exception as e:
            print("Erro ao extrair score:", e)
            score = 0.0

        if score > 0.7:
            filtered_plots.append(plot)

    state["plots"] = filtered_plots
    return state

pdf_report_llm = get_pdf_report_agent()

def generate_pdf_report_node(state: DataAnalysisState) -> DataAnalysisState:
    stats = state.get("eda_summary", "")
    user_input = state.get("input", "")
    plots = state.get("plots", [])

    str_plots = format_plots_for_agent_plain(plots=plots)

    agent_input = {
        "stats": stats,
        "plots": str_plots,
        "user_input": user_input
    }

    print("agente gerador de markdown")
    response = pdf_report_llm.invoke(agent_input).content
    report_markdown = extract_markdown(response)

    print("gerador de pdf a partir do markdown")
    pdf_path = generate_pdf_from_markdown(report_markdown)

    return {
        **state,
        "pdf_path": pdf_path
    }

