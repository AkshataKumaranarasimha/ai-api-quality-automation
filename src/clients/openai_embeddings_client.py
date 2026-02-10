import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# --- FORCE load .env from project root ---
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


class OpenAIEmbeddingsClient:
    """
    OpenAI Embeddings client.
    Explicitly passes api_key to avoid env-loading ambiguity.
    """

    def __init__(self, model: str = None):
        self.model = model or os.getenv(
            "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
        )

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY not found. Check .env loading."
            )

        # ✅ THIS is the critical fix
        self.client = OpenAI(api_key=api_key)

    def embed(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding


'''
if __name__ == "__main__":
    emb = OpenAIEmbeddingsClient()
    vec = emb.embed("GET_VEHICLE_INSURANCE_OFFERS")

    print("\n[EMBEDDING SANITY CHECK]")
    print("Model:", emb.model)
    print("Vector length:", len(vec))
    print("First 5 values:", vec[:5])
'''