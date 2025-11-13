from langchain_openai import AzureChatOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import os
from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv(
    "AZURE_OPENAI_ENDPOINT", "https://eus2aoairecrewtor.openai.azure.com"
)
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5-nano")

scope = "https://cognitiveservices.azure.com/.default"
token_provider = get_bearer_token_provider(DefaultAzureCredential(), scope)


def make_llm() -> AzureChatOpenAI:
    return AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,
        azure_ad_token_provider=token_provider,
    )


# execution guards / performance toggles
MAX_STEPS = int(os.getenv("MAX_STEPS", "12"))
FAST_PATH_ENABLED = True  # skip retrieval if plan says no data
