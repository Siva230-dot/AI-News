import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    GROQ_API_KEY: str = os.getenv(
        "GROQ_API_KEY",
        ""
    )

    GROQ_MODEL: str = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-20b"
    )

    HF_TOKEN: str = os.getenv(
        "HF_TOKEN",
        ""
    )

    HF_MODEL: str = os.getenv(
        "HF_MODEL",
        "meta-llama/Llama-3.1-8B-Instruct"
    )

    TELEGRAM_API_ID: str = os.getenv(
        "TELEGRAM_API_ID",
        ""
    )

    TELEGRAM_API_HASH: str = os.getenv(
        "TELEGRAM_API_HASH",
        ""
    )


settings = Settings()