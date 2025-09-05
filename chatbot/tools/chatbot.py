from pydantic import BaseModel, Field
from typing import Literal, Optional

class RouteSupervisor(BaseModel):
    goto: Literal["sql", "analysis"] = Field(
        ...,
        description="Destino de encaminhamento. Use 'sql' para encaminhar para o agente SQL ou 'analysis' para análise."
    )
    message: str = Field(
        ...,
        description=(
            "Mensagem para o agente encaminhado. "
            "Se 'goto' for 'sql', deve ser uma pergunta em linguagem natural sobre os dados. "
            "Se 'goto' for 'analysis', deve ser uma descrição da análise a ser realizada."
        )
    )

