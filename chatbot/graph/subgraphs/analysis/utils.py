import base64
from io import BytesIO
from PIL import Image
import re
import os
from chatbot.schemas.schemas import PlotWithAnalysis

def convert_to_base64(image_path):
    pil_image = Image.open(image_path)
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


def extract_python_code(markdown_text: str) -> str:
    match = re.search(r"```python\s*(.*?)```", markdown_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

def extract_markdown(markdown_text: str) -> str:
    match = re.search(r"```markdown\s*(.*?)```", markdown_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

def format_plots_for_agent_plain(plots: list[PlotWithAnalysis]) -> str:
    formatted = []

    for i, plot in enumerate(plots, start=1):
        filename = os.path.basename(plot["path"])  
        description = plot.get("description", "")
        analysis = plot.get("analysis", "")

        plot_str = (
            f"Gráfico {i}\n"
            f"path: {filename}\n"
            f"description: {description}\n"
            f"analise: {analysis}\n"
            f"{'='*25}"
        )
        formatted.append(plot_str)

    return "\n".join(formatted)