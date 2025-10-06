import streamlit as st
import os
from databot.run import run_databot

# -------------------------
# Configuração da página
# -------------------------
st.set_page_config(
    page_title="databot com CSV",
    page_icon="💬",
    layout="wide"
)

st.title("💬 databot com LangGraph")
st.caption("Interaja com seus dados em CSV usando IA")

# Pasta para salvar CSVs
CSV_FOLDER = "databot/data/csv"
os.makedirs(CSV_FOLDER, exist_ok=True)

# -------------------------
# Sidebar: upload de CSV
# -------------------------
with st.sidebar:
    st.header("📁 Arquivo de Dados")
    csv_file = st.file_uploader("Envie um CSV (opcional)", type=["csv"])
    csv_path = None
    if csv_file is not None:
        csv_path = os.path.join(CSV_FOLDER, csv_file.name)
        with open(csv_path, "wb") as f:
            f.write(csv_file.getbuffer())
        st.success(f"CSV salvo em: `{csv_path}`")

# -------------------------
# Histórico visual
# -------------------------
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# Entrada do usuário
# -------------------------
if prompt := st.chat_input("Digite sua mensagem..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.mensagens.append({"role": "user", "content": prompt})

    try:
        resultado = run_databot(prompt, csv_path=csv_path)
        markdown_text = resultado.get("markdown")
        pdf_path = resultado.get("pdf_path")
        csv_path_bot = resultado.get("csv_path")
    except:
        markdown_text = None
        pdf_path = None
        csv_path_bot = None

    if not markdown_text:
        task = resultado.get("task")
        print(task)
        if task and task.get("subgraph") == "END":
            markdown_text = task.get("description", "Erro ao gerar mensagem. Por favor, repita o pedido")
        else:
            markdown_text = "Erro ao gerar mensagem. Por favor, repita o pedido."

    with st.chat_message("assistant"):
        st.markdown(markdown_text, help="Resposta gerada pelo databot")

        col1, col2 = st.columns(2)
        with col1:
            if pdf_path and os.path.exists(pdf_path):
                st.markdown("**📄 PDF gerado:**")
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="Baixar PDF",
                        data=f,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )

        with col2:
            if csv_path_bot and not csv_path and os.path.exists(csv_path_bot):
                st.markdown("**📊 CSV gerado:**")
                with open(csv_path_bot, "r") as f:
                    csv_text = f.read()
                st.download_button(
                    label="Baixar CSV",
                    data=csv_text,
                    file_name=os.path.basename(csv_path_bot),
                    mime="text/csv",
                    type="primary",
                    use_container_width=True
                )
                with st.expander("🔍 Visualizar CSV"):
                    st.code(csv_text, language="csv")

    st.session_state.mensagens.append({"role": "assistant", "content": markdown_text})
