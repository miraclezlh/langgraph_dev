from typing import TypedDict

from langchain_core.messages import AnyMessage, AIMessage, HumanMessage
from langgraph.constants import START
from langgraph.graph import StateGraph, MessagesState

# 节点starter

# 定义节点间交互的状态类
class State(TypedDict):
    message: list[AnyMessage]
    extra_field: int


def node(state: MessagesState):
    messages = state["messages"]
    new_message = AIMessage(content="您好！我是节点1！")

    return {
        "messages": messages + [new_message],
        "extra_field": 1
    }


builder = StateGraph(MessagesState)
builder.add_node("agent", node)

builder.add_edge(START,"agent")

graph = builder.compile()

# Mermaid是基于文本的图表，和流程图的可视化工具
# display(Image(graph.get_graph().draw_mermaid_png()))

result = graph.invoke({
    "messages": [HumanMessage(content="您好啊！我是Tom！")]
})

print(result)
