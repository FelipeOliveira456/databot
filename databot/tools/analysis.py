import pandas as pd
import matplotlib.pyplot as plt
import pypandoc
import seaborn as sns
import uuid, os, copy
import datetime
from pathlib import Path
from databot.graph.subgraphs.analysis.utils import convert_to_base64

DATABOT_DIR = Path.cwd() / "databot"

PLOT_DIR =  DATABOT_DIR / "data" / "img"
PDF_DIR = DATABOT_DIR / "data" / "pdf"
os.makedirs(PLOT_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

def _save_fig_to_file() -> str:
    """Salva a figura atual como imagem PNG em um arquivo temporário."""
    filename = f"{uuid.uuid4().hex}.png"
    path = os.path.join(PLOT_DIR, filename)
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    return path

def execute_plot_code(df: pd.DataFrame, code: str) -> dict:
    """
    Executa código Python de plot gerado pelo LLM, garantindo que não use comandos proibidos,
    não modifique o DataFrame original, salva a figura e retorna o caminho.
    """
    banned_keywords = [
        "os.", "sys.", "subprocess", "eval", "exec", "open", "importlib",
        "plt.savefig", "plt.close"
    ]

    for word in banned_keywords:
        if word in code:
            raise ValueError(f"Código contém comando proibido: {word}")

    df_copy = copy.deepcopy(df)
    exec_namespace = {
        "df": df_copy,
        "plt": plt,
        "sns": sns,
        "pd": pd
    }

    exec(code, exec_namespace)

    path = _save_fig_to_file()
    return {"path": path}

def generate_pdf_from_markdown(markdown_text: str) -> str:
    """
    Converte um texto em Markdown para PDF usando pypandoc.
    As imagens no Markdown devem estar no diretório PLOT_DIR ou com caminho absoluto.
    Retorna o caminho do PDF gerado.
    """
    processed_md = markdown_text
    for file in os.listdir(PLOT_DIR):
        abs_path = os.path.join(PLOT_DIR, file)
        if file in processed_md:
            processed_md = processed_md.replace(f"({file})", f"({abs_path})")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"relatorio_{timestamp}.pdf"
    pdf_path = os.path.join(PDF_DIR, pdf_filename)

    pypandoc.convert_text(
        processed_md,
        'pdf',
        format='md',
        outputfile=pdf_path,
        extra_args=['--standalone']
    )

    return pdf_path, processed_md

def embed_plots_in_markdown(markdown_text: str, plots: list) -> str:
    """
    Substitui caminhos de imagens no markdown por base64 usando convert_to_base64.
    
    Args:
        markdown_text (str): Markdown original.
        plots (list): Lista de PlotWithAnalysis, cada um com 'path'.
    
    Returns:
        str: Markdown com imagens em base64.
    """
    if not markdown_text or not plots:
        return markdown_text

    for plot in plots:
        path = plot["path"]
        if path in markdown_text:
            img_base64 = convert_to_base64(path)
            markdown_text = markdown_text.replace(path, f"data:image/png;base64,{img_base64}")
    
    return markdown_text

# def plot_histogram(df: pd.DataFrame, column: str, bins: int = 30) -> dict:
#     plt.figure()
#     sns.histplot(df[column].dropna(), bins=bins, kde=True)
#     plt.title(f"Histograma de {column}")
#     plt.xlabel(column)
#     plt.ylabel("Frequência")
#     path = _save_fig_to_file()
#     return {
#         "image_path": path,
#         "description": f"Histograma da coluna '{column}'."
#     }

# def plot_bar(df: pd.DataFrame, x: str, y: str) -> dict:
#     plt.figure()
#     grouped = df.groupby(x)[y].mean().reset_index()
#     sns.barplot(data=grouped, x=x, y=y)
#     plt.title(f"Gráfico de Barras: {y} por {x}")
#     path = _save_fig_to_file()
#     return {
#         "image_path": path,
#         "description": f"Gráfico de barras de '{y}' por '{x}', usando média dos valores."
#     }

# def plot_scatter(df: pd.DataFrame, x: str, y: str, hue: str = None) -> dict:
#     plt.figure()
#     sns.scatterplot(data=df, x=x, y=y, hue=hue)
#     plt.title(f"Dispersão entre {x} e {y}")
#     desc = f"Gráfico de dispersão entre '{x}' e '{y}'"
#     if hue:
#         desc += f", colorido por '{hue}'"
#     path = _save_fig_to_file()
#     return {
#         "image_path": path,
#         "description": desc + "."
#     }

# def plot_boxplot(df: pd.DataFrame, x: str, y: str) -> dict:
#     plt.figure()
#     sns.boxplot(data=df, x=x, y=y)
#     plt.title(f"Boxplot de {y} por {x}")
#     path = _save_fig_to_file()
#     return {
#         "image_path": path,
#         "description": f"Boxplot da variável '{y}' agrupada por '{x}'."
#     }

# def plot_correlation_matrix(df: pd.DataFrame) -> dict:
#     plt.figure(figsize=(10, 8))
#     corr = df.corr(numeric_only=True)
#     sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
#     plt.title("Matriz de Correlação")
#     path = _save_fig_to_file()
#     return {
#         "image_path": path,
#         "description": "Matriz de correlação entre colunas numéricas."
#     }
