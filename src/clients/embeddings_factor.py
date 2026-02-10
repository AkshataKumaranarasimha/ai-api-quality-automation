import os

from src.clients.sklearn_embeddings_client import SklearnEmbeddingsClient
from src.clients.openai_embeddings_client import OpenAIEmbeddingsClient


def get_embeddings_client():
    """
    Factory to return the embeddings client.

    EMBEDDINGS_PROVIDER:
      - "sklearn" (default, offline, CI-safe)
      - "openai"  (requires API key + quota)
    """
    provider = os.getenv("EMBEDDINGS_PROVIDER", "sklearn").lower()

    if provider == "openai":
        return OpenAIEmbeddingsClient()

    if provider == "sklearn":
        return SklearnEmbeddingsClient()

    raise ValueError(f"Unsupported EMBEDDINGS_PROVIDER: {provider}")
