from typing import Annotated
from langgraph.graph.message import AnyMessage, add_messages
from typing_extensions import TypedDict, NotRequired, Literal
import pandas as pd

class BaseState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

class Task(TypedDict):
    subgraph: Literal["sql", "analysis"]  
    description: str  

class SupervisorState(TypedDict):
    input: str
    task: NotRequired[Task]
    tasks_list: NotRequired[list[Task]]
    csv_path: NotRequired[str]
    pdf_path: NotRequired[str]
    markdown: NotRequired[str]

class PlotWithAnalysis(TypedDict):
    path: str    
    description: str
    analysis: NotRequired[str]

class DataAnalysisState(TypedDict, total=False):
    input: str
    df: pd.DataFrame                      
    eda_summary: NotRequired[str]
    planned_plots: NotRequired[list[str]]
    tool_calls: NotRequired[str]       
    plots: NotRequired[list[PlotWithAnalysis]] 
    pdf_path: NotRequired[str]
    markdown: NotRequired[str]



