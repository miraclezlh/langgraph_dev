from langchain.chat_models import init_chat_model

"""
    创建各类LLM大模型
"""

# langchain整合了初始化模型，init_chat_model
ollama_llm_qwen = init_chat_model(
    api_key="ollama",
    base_url="http://localhost:11434",
    model='qwen3:8b',
    model_provider='ollama'
)

ollama_llm_qwen3_4b = init_chat_model(
    api_key="ollama",
    base_url="http://localhost:11434",
    model='qwen3:4b',
    model_provider='ollama'
)

ollama_llm_gemma = init_chat_model(
    api_key="ollama",
    base_url="http://localhost:11434",
    model='gemma4:e2b',
    model_provider='ollama'
)
