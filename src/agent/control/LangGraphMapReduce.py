import operator
from typing import TypedDict, Annotated

from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Send
from pydantic import BaseModel, Field

from llm_init import ollama_llm_qwen

# 如果需要序列化核心对象（更通用的选择）
serializer = JsonPlusSerializer(allowed_objects='core')


# 模型和提示词
# 定义我们将使用的模型和提示词
subjects_prompt = """ 生成一个逗号分隔的列表，包含2到5个与以下主题相关的例子：{topic}。 """
joke_prompt = """ 生成一个关于{subject}的笑话 """
best_joke_prompt = """ 以下是一些关于{topic}的笑话。选出最好的一个！返回最佳笑话的ID。 {jokes}"""


class Subjects(BaseModel):
    subject: list[str]


class Joke(BaseModel):
    joke: str


class BestJoke(BaseModel):
    id: int = Field(description="最佳笑话的索引，从0开始", ge=0)


# 这将是主图的整体状态
# 它将包含一个主题（我们期望用户提供）
# 然后将生成一个主题列表，并为每个主题生成一个笑话
class OverallState(TypedDict):
    topic: str
    subjects: list
    # 注意这里我们使用operator.add
    # 这是因为我们想把从各个节点生成的所有笑话
    # 合并回一个列表，这本质上是"规约"部分
    jokes: Annotated[list, operator.add]
    best_selected_joke: str


# 用于生成笑话
class JokeState(TypedDict):
    subject: str


# 这是我们用来生成笑话主题的函数
def generate_topics(state: OverallState):
    prompt = subjects_prompt.format(topic=state["topic"])
    response = ollama_llm_qwen.with_structured_output(Subjects).invoke(prompt)
    # 模型返回AIMessage，可以用"."来获取字段
    return {"subjects": response.subjects}


# 这是我们根据给定的主题，生成笑话
def generate_joke(state: JokeState):
    prompt = joke_prompt.format(subject=state["subject"])
    response = ollama_llm_qwen.with_structured_output(Subjects).invoke(prompt)
    # 模型返回AIMessage，可以用"."来获取字段
    return {"jokes": [response.jokes]}


# 这是我们定义映射到生成的主题上的逻辑
# 我们将在图中使用这个作为边缘
def continue_to_jokes(state: OverallState):
    # 我们将返回一个'Send'对象列表
    # 每个'Send'对象包含图中节点的名称
    # 以及要发送到该节点的状态
    return [Send("generate_joke", {"subject": s}) for s in state["subjects"]]


# 这里我们将评判最佳笑话
def best_joke(state: OverallState):
    jokes = "\n\n".join(state["jokes"])
    prompt = best_joke_prompt.format(topic=state["topic"], jokes=jokes)
    response = ollama_llm_qwen.with_structured_output(BestJoke).invoke(prompt)
    # 模型返回AIMessage，可以用"."来获取字段
    return {"best_selected_joke": state["jokes"][response.id]}


# 构建图：这里我们将所有内容组合在一起
graph = StateGraph(OverallState)
graph.add_node("generate_topics", generate_topics)
graph.add_node("generate_joke", generate_joke)
graph.add_node("best_joke", best_joke)

graph.add_edge(START, "generate_topics")
graph.add_conditional_edges("generate_topics", continue_to_jokes, ["generate_joke"])
graph.add_edge("generate_joke", "best_joke")
graph.add_edge("best_joke", END)
app = graph.compile()

#
# # Mermaid是基于文本的图表，和流程图的可视化工具
# try:
#     # 使用 Mermaid 生成图表并保存为文件
#     mermaid_code = graph.get_graph().draw_mermaid_png()
#     with open("best_joke.jpg", "wb") as f:
#         f.write(mermaid_code)
#
#     # 使用 matplotlib 显示图像
#     img = mpimg.imread("best_joke.jpg")
#     plt.imshow(img)
#     plt.axis('off')  # 关闭坐标轴
#     plt.show()
# except Exception as e:
#     print(f"An error occurred: {e}")
