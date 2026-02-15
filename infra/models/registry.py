from enum import Enum


class Models(str, Enum):
    QWEN = "qwen"
    DEEPSEEK = "deepseek"
    MISTRAL = "mistral"
    QWEN_JUDGE = 'qwen_judge'
    LLAMA_JUDGE = 'llama_judge'
    ALL = "all"


MODEL_REGISTRY = {
    Models.QWEN: "Qwen/Qwen2.5-7B-Instruct:together",
    Models.DEEPSEEK: "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
    Models.MISTRAL: "mistralai/Mistral-7B-Instruct-v0.3",
    Models.QWEN_JUDGE: "Qwen/Qwen2.5-32B-Instruct",
    Models.LLAMA_JUDGE: "meta-llama/Llama-3.1-70B-Instruct",
}

def resolve_models(selected):
    if Models.ALL in selected:
        return list(MODEL_REGISTRY.values())
    
    return [MODEL_REGISTRY[Models[s]] for s in selected]