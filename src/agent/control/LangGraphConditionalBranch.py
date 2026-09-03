import operator
from typing import TypedDict, Annotated, Literal

import matplotlib.image as mpimg
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from matplotlib import pyplot as plt

# 条件分支的例子

# 定义节点间交互的状态类
# Annotated允许为类型，提供额外的元数据；而不影响类型检查
class State(TypedDict):
    aggregate: Annotated[list, operator.add]


def a(state: State):
    print(f"添加'A'到{state['aggregate']}")
    return {"aggregate": ["A"]}


def b(state: State):
    print(f"添加'B'到{state['aggregate']}")
    return {"aggregate": ["B"]}

def route(state: State) -> Literal["b",END]:
    if len(state["aggregate"]) <7 :
        return "b"
    else:
        return END



builder = StateGraph(State)
builder.add_node(a)
builder.add_node(b)


builder.add_edge(START, "a")
builder.add_conditional_edges("a",route)
builder.add_edge("b", "a")
graph = builder.compile()

# Mermaid是基于文本的图表，和流程图的可视化工具
try:
    # 使用 Mermaid 生成图表并保存为文件
    mermaid_code = graph.get_graph().draw_mermaid_png()
    with open("conditional_graph.jpg", "wb") as f:
        f.write(mermaid_code)

    # 使用 matplotlib 显示图像
    img = mpimg.imread("conditional_graph.jpg")
    plt.imshow(img)
    plt.axis('off')  # 关闭坐标轴
    plt.show()
except Exception as e:
    print(f"An error occurred: {e}")

result = graph.invoke({"aggregate": []}, {"configurable": {"thread_id": "test"}})
print(result)
