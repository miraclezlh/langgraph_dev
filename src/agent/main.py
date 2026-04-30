from typing import TypedDict

from langchain.chat_models import init_chat_model
from langgraph.constants import START, END
from langgraph.graph import StateGraph


# 定义图的状态State，是LangGraph的灵魂，所有节点共享，通过它进行读写，来传递信息
class State(TypedDict):
    """图的状态定义"""
    user_input: str      # 用户输入的问题
    response: str       # AI的回答

# 初始化LLM大模型
ollama_llm_qwen = init_chat_model(
    api_key="ollama",
    base_url="http://localhost:11434",
    model='qwen3:8b',
    model_provider='ollama'
)

# 定义节点函数，每个节点都是一个函数，输入是state，输出是更新后的state
def chat_node(state: State) -> State:
    """
        聊天节点，接收用户问题，调用LLM，返回问答
        :param state: 当前图的状态，包含user_input
        :return: 更新后的状态，包含response
    """

    # 从状态中获取用户输入
    user_input = state["user_input"]

    # 调用大模型，获取输出信息
    resp = ollama_llm_qwen.invoke(user_input)

    return {"response":resp.content}

# 创建StateGraph实例
builder = StateGraph(State)

builder.add_node("chat",chat_node)

# 添加START起始边
builder.add_edge(START,"chat")

# 添加END结束边
builder.add_edge("chat",END)

# 编译图，做了三件事：拓扑图校验；生成执行计划；初始化状态控件
graph= builder.compile()


if __name__ == "__main__":
    user_question ="介绍一下你自己"

    result = graph.invoke({"user_input":user_question})

    print("="*50)
    print(f"你问:{user_question}")
    print("-"*50)
    print(f"AI回答:{result['response']}")
    print("="*50)











