from typing import TypedDict

from IPython.display import Image,display
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage
from langgraph.graph import StateGraph, MessagesState
from langgraph.constants import START, END

# 定义节点间交互的状态类
class State(TypedDict):
    value_1: str
    value_2: str


def step_1(state: State):
    print(f"state:\n {state}")
    return {"value_1":"a"}

def step_2(state: State):
    current_value_1 = state["value_1"]
    return {"value_1":f"{current_value_1}+b"}

def step_3(state: State):
    return {"value_1":10}

builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("step_2", step_2)
builder.add_node("step_3", step_3)

builder.add_edge(START,"step_1")
builder.add_edge("step_1","step_2")
builder.add_edge("step_2","step_3")
builder.add_edge("step_3",END)

graph = builder.compile()

# Mermaid是基于文本的图表，和流程图的可视化工具
display(Image(graph.get_graph().draw_mermaid_png()))

result = graph.invoke({"value_1":"a"})

print(result)