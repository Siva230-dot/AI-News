from app.gateway.providers.groq_provider import get_groq_llm
from app.gateway.providers.huggingface_provider import get_huggingface_llm
from app.config.settings import settings


class AIGateway:

    def __init__(self):
        # Primary provider
        self.groq = get_groq_llm()

        # Fallback provider
        self.huggingface = None

        if settings.HF_TOKEN:
            try:
                self.huggingface = get_huggingface_llm()
                print("Hugging Face fallback initialized.")
            except Exception as e:
                print(f"Hugging Face initialization failed: {e}")

    def get_groq(self):
        return self.groq

    def get_huggingface(self):
        return self.huggingface

    async def generate(self, messages):
        """
        Primary: Groq
        Fallback: Hugging Face
        """

        # Try Groq first
        try:
            response = await self.groq.ainvoke(messages)

            print("AI Gateway: Groq used")

            return response.content

        except Exception as groq_error:

            print(f"Groq failed: {groq_error}")
            print("AI Gateway: Switching to Hugging Face...")

            # Try Hugging Face
            if self.huggingface is None:
                raise RuntimeError(
                    "Groq failed and Hugging Face fallback is not configured."
                )

            try:
                response = await self.huggingface.chat_completion(
                    messages=messages,
                    model=settings.HF_MODEL,
                    temperature=0,
                    max_tokens=1500,
                )

                print("AI Gateway: Hugging Face used")

                return response.choices[0].message.content

            except Exception as hf_error:

                raise RuntimeError(
                    f"Both AI providers failed. "
                    f"Groq: {groq_error} | "
                    f"Hugging Face: {hf_error}"
                )


gateway = AIGateway()