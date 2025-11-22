from langchain_openai import AzureChatOpenAI
from langchain_ollama import ChatOllama
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from typing import Union
import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")

AZURE_OPENAI_ENDPOINT = os.getenv(
    "AZURE_OPENAI_ENDPOINT", "https://eus2aoairecrewtor.openai.azure.com"
)
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5-nano")

scope = "https://cognitiveservices.azure.com/.default"
token_provider = get_bearer_token_provider(DefaultAzureCredential(), scope)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "openchat:7b")
# OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1:7b")


def make_llm() -> Union[AzureChatOpenAI, ChatOllama]:
    if LLM_PROVIDER == "azure":
        return AzureChatOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_deployment=AZURE_OPENAI_DEPLOYMENT,
            azure_ad_token_provider=token_provider,
        )

    # default: local Ollama
    return ChatOllama(
        base_url=OLLAMA_BASE_URL,
        model=OLLAMA_MODEL,
        temperature=0,
    )


# def make_llm() -> AzureChatOpenAI:
#     return AzureChatOpenAI(
#         azure_endpoint=AZURE_OPENAI_ENDPOINT,
#         api_version=AZURE_OPENAI_API_VERSION,
#         azure_deployment=AZURE_OPENAI_DEPLOYMENT,
#         azure_ad_token_provider=token_provider,
#     )


# execution guards / performance toggles
MAX_STEPS = int(os.getenv("MAX_STEPS", "12"))
FAST_PATH_ENABLED = True  # skip retrieval if plan says no data
