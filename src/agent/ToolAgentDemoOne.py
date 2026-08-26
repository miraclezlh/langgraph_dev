# 第一步：导入包
from datetime import datetime
from typing import TypedDict

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.constants import START, END
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

# 第二步：对本python文件的功能进行注释
# ========================
# LangGraph进阶调用：带工具调用的只能Agent
# 功能：大模型自动判断，是否需要调用工具（计算器/获取时间）
# 架构：ReAct 模式 Reasoning思考 Acting行动
# 版本LangGraph      LangChain
# ========================
@tool
def calculator(expression: str) -> str:
    """计算数学表达式的结果。当用户需要做数学计算时，可以调用此工具。支持加减乘除运算。

    :param expression: 需要进行计算的数学表达式字符串，例如'2+3*6','(3+5)/2','2*3*6'
    :return: 字符串
    """

    try:
        # 定义无序且不重复的集合set
        allowed_chars = set("0123456789+-*/()[].e")
        # for 变量 in 表达式
        # all用于判断，表达式中所有值是否都是真值
        if not all(c in allowed_chars for c in expression):
            return "错误：表达式包含不允许的字符"

        result = eval(expression)
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"计算错误：{str(e)}"


@tool
def get_current_time(input: str="") -> str:
    """获取当前时间，当用户需要获取当前时间，可以进行请求

    :param input: 冗余参数，暂时不需要
    :return: 字符串
    """

    now = datetime.now()
    return f"当前时间：{now.strftime('%Y年%m月%d日 %H:%M:%S')} 星期{['一','二','三','四','五','六','日'][now.weekday()]}"

tools = [calculator,get_current_time]

# 第四步：初始化LLM大模型，并绑定tool
ollama_llm_qwen = init_chat_model(
    api_key="ollama",
    base_url="http://localhost:11434",
    model='qwen3:8b',
    model_provider='ollama'
)
llm_with_tools = ollama_llm_qwen.bind_tools(tools)

# 第五步：定义节点函数，agent节点
def agent_node(state:MessagesState) -> dict:
    print("--------------")

    print(state)
    # State 系统会自动追加AIMessage，ToolMessage等到messages列表里
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    # response返回的是AIMessage
    print(response)

    print("--------------")
    return {"messages":[response]}


# ToolNode是LangGraph内置的工具执行节点
# 传入工具列表，它会自动：
# 1.从AIMessage获取tool_calls
# 2.找到对应的工具函数
# 3.执行工具函数
# 4.把执行结果包装成ToolMessage 并进行返回
tool_node = ToolNode(tools)


# 第六步：定义条件路由函数
def should_continue(state : MessagesState) -> str:
    # 获取最后一条信息，通常是AIMessage
    last_message = state["messages"][-1]
    if hasattr(last_message,"tool_calls") and last_message.tool_calls:
        return "forward_tools_node"
    return "__end__"

# 第七步：构建流程图
builder = StateGraph(MessagesState)
# 添加节点
builder.add_node("agent",agent_node)  # agent节点函数
builder.add_node("tools",tool_node)   # tool工具节点

# 添加开始边，START节点到agent节点
builder.add_edge(START,"agent")
# 添加条件路由边
builder.add_conditional_edges(
    "agent",
    should_continue,
    {"forward_tools_node":"tools","__end__":END}
)
# 工具执行完毕后，回到agent节点继续推理
builder.add_edge("tools","agent")

# 对图进行编译
graph = builder.compile()

# 第八步：运行
def chat_with_debug(user_input: str):
    print(f"\n{'='*60}")
    print(f"用户问题：{user_input}")
    print(f"\n{'='*60}")

    # graph返回的result是json字符串，key为messages，value为消息列表
    result = graph.invoke(
        {"messages":[HumanMessage(content=user_input)]},
        config={"configurable":{"thread_id":"debug"}}
    )

    # 推理结束，开始解析
    print(f"graph返回的result为：{result}")
    print(f"返回message的数量：{len(result['messages'])}")

    # 展示所有中间的流程
    for i,msg in enumerate(result["messages"]):
        if isinstance(msg,HumanMessage):
            print(f"\n[步骤{i}] 用户输入")
            print(f"内容：{msg.content}")
        elif isinstance(msg,AIMessage):
            if msg.tool_calls:
                # 大模型判断，需要调用tool
                print(f"\n[步骤{i}] agent决定调用工具")
                for tc in msg.tool_calls:
                    print(f"   工具： {tc['name']}")
                    print(f"   参数： {tc['args']}")
            else:
                # 最终的答案
                print(f"\n[步骤{i}] agent最终回答")
                print(f"内容 {msg.content}")
        elif isinstance(msg,ToolMessage):
            print(f"\n[步骤{i}] 工具执行结果")
            print(f"   工具： {msg.name}")
            print(f"   内容： {msg.content}")

    print(f"\n{'='*60}")
    print(f"最终的回答：{result['messages'][-1].content}")
    print(f"\n{'='*60}")

# 第九步
if __name__ == '__main__':
    # 数学计算测试
    print("测试1: 数学计算")
    chat_with_debug("25乘以10等于多少？然后再加上12，等于多少？")


