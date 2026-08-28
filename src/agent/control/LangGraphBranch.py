import operator
from typing import TypedDict, Annotated

from fastapi import FastAPI
# from langgraph_sdk import get_langgraph_server
from IPython.display import Image,display
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage
from langgraph.graph import StateGraph, MessagesState
from langgraph.constants import START, END

# 定义节点间交互的状态类
# Annotated允许为类型，提供额外的元数据；而不影响类型检查
class State(TypedDict):
    aggregate: Annotated[list,operator.add]


def a(state: State):
    print(f"添加'A'到{state['aggregate']}")
    return {"aggregate":["A"]}

def b(state: State):
    print(f"添加'B'到{state['aggregate']}")
    return {"aggregate":["B"]}

def c(state: State):
    print(f"添加'C'到{state['aggregate']}")
    return {"aggregate":["C"]}

def d(state: State):
    print(f"添加'D'到{state['aggregate']}")
    return {"aggregate":["D"]}

builder = StateGraph(State)
builder.add_node(a)
builder.add_node(b)
builder.add_node(c)
builder.add_node(d)

builder.add_edge(START,"a")
builder.add_edge("a","b")
builder.add_edge("a","c")
builder.add_edge("b","d")
builder.add_edge("c","d")
builder.add_edge("d",END)

graph = builder.compile()

# Mermaid是基于文本的图表，和流程图的可视化工具
display(Image(graph.get_graph().draw_mermaid_png()))


# app = FastAPI()
# # 注册调试服务
# app.include_router(get_langgraph_server(graph), prefix="/langgraph")
#
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8123)


