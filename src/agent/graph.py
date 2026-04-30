
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama

# langchain整合了初始化模型，init_chat_model
ollama_llm_qwen = init_chat_model(
    api_key="ollama",
    base_url="http://localhost:11434",
    model='qwen3:8b',
    model_provider='ollama'
)


def get_weather(city: str) -> str:
    # 模拟天气查询
    """获取给定城市的天气。"""
    return f"{city} 天气晴朗！"


"""
    创建agent，调用工具回答用户问题
"""

# 创建Agent智能体
graph = create_agent(
    model=ollama_llm_qwen,
    tools=[get_weather],
    system_prompt="你是一个助手，你可以查询城市的天气。"
)