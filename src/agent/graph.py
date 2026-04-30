
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama

ollama_llm = ChatOllama(
    base_url="http://localhost:11434",
    model='qwen3:8b'
)

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
agent = create_agent(
    model=ollama_llm,
    tools=[get_weather],
    system_prompt="你是一个助手，你可以查询城市的天气。"
)

# 通过Agent调用LLM
resp = agent.invoke(
    {"messages": [{"role": "user", "content": "查询北京的天气"}]}
)
print(resp)

# 返回的是agent的结构体
"""
{
    'messages': [
        HumanMessage(content='查询北京的天气', additional_kwargs={}, response_metadata={}, id='8c2ba2e4-8518-461d-a38d-ba5682acb7af'), 
        AIMessage(content='<think>\n好的，用户让我查询北京的天气。我需要使用提供的工具来完成这个任务。首先，检查工具部分，看到有一个get_weather函数，参数是城市名。用户已经明确提到“北京”，所以参数应该是city: "北京"。接下来，我需要确保正确调用这个函数，返回对应的天气信息。没有其他参数需要处理，直接调用即可。\n</think>\n\n', additional_kwargs={}, response_metadata={'model': 'qwen3:8b', 'created_at': '2026-04-16T14:43:22.828895Z', 'done': True, 'done_reason': 'stop', 'total_duration': 21946210500, 'load_duration': 3484844700, 'prompt_eval_count': 150, 'prompt_eval_duration': 7363977200, 'eval_count': 103, 'eval_duration': 11050966100, 'logprobs': None, 'model_name': 'qwen3:8b', 'model_provider': 'ollama'}, id='lc_run--019d96be-d08d-7d83-b1e2-c83425c79594-0', tool_calls=[{'name': 'get_weather', 'args': {'city': '北京'}, 'id': '71b38ec6-de7f-47c1-b882-4548ee55ede6', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 150, 'output_tokens': 103, 'total_tokens': 253}), 
        ToolMessage(content='北京 天气晴朗！', name='get_weather', id='f959df5f-ac1b-4384-b1f6-018d88da5086', tool_call_id='71b38ec6-de7f-47c1-b882-4548ee55ede6'), 
        AIMessage(content='<think>\n</think>\n\n北京的天气晴朗，适合外出活动！', additional_kwargs={}, response_metadata={'model': 'qwen3:8b', 'created_at': '2026-04-16T14:43:25.9174622Z', 'done': True, 'done_reason': 'stop', 'total_duration': 3020223200, 'load_duration': 189514800, 'prompt_eval_count': 254, 'prompt_eval_duration': 972818600, 'eval_count': 15, 'eval_duration': 1850887700, 'logprobs': None, 'model_name': 'qwen3:8b', 'model_provider': 'ollama'}, id='lc_run--019d96bf-268d-7fd1-a01f-385cfd3ed2f9-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 254, 'output_tokens': 15, 'total_tokens': 269})
    ]
}
"""

# 创建Agent
agent_two = create_agent(
    model=ollama_llm_qwen,
    tools=[get_weather],
    system_prompt="你是一个助手，你可以查询城市的天气。"
)
# 通过Agent调用LLM
resp_two = agent_two.invoke(
    {"messages": [{"role": "user", "content": "查询北京的天气"}]}
)
print(resp_two)
