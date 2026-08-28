import operator
from typing import TypedDict, Annotated

from fastapi import FastAPI
# from langgraph_sdk import get_langgraph_server
from IPython.display import Image,display
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage
from langgraph.graph import StateGraph, MessagesState
from langgraph.constants import START, END
from matplotlib import pyplot as plt
import matplotlib.image as mpimg


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
try:
    # 使用 Mermaid 生成图表并保存为文件
    mermaid_code = graph.get_graph().draw_mermaid_png()
    with open("graph.jpg", "wb") as f:
        f.write(mermaid_code)

    # 使用 matplotlib 显示图像
    img = mpimg.imread("graph.jpg")
    plt.imshow(img)
    plt.axis('off')  # 关闭坐标轴
    plt.show()
except Exception as e:
    print(f"An error occurred: {e}")



