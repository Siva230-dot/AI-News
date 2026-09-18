from huggingface_hub import AsyncInferenceClient
from app.config.settings import settings


def get_huggingface_llm():

    if not settings.HF_TOKEN:
        raise ValueError(
            "HF_TOKEN is not configured."
        )

    return AsyncInferenceClient(
        provider="auto",
        api_key=settings.HF_TOKEN,
    )