from pydantic import BaseModel, Field
from typing import Literal

class RouteSupervisor(BaseModel):
    """
    Roteador de decisão entre nós de agentes.

    Esta ferramenta é usada para determinar o próximo passo no fluxo da conversa
    e definir a mensagem a ser repassada para outro agente (por exemplo, um agente SQL).

    Use esta ferramenta apenas quando a mensagem não for destinada ao usuário humano
    que está interagindo com o chatbot. Se a mensagem for para o humano,
    não use esta ferramenta — responda diretamente.
    """

    goto: Literal["sql"] = Field(
        ...,
        description="Destino de encaminhamento. Use 'sql' para encaminhar para o agente SQL."
    )
    message: str = Field(
        description="Uma pergunta em linguagem natural sobre os dados. Não inclua código SQL ou Python."
    )

