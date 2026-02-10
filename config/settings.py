import os
from dotenv import load_dotenv

load_dotenv()

AI_API_BASE_URL = os.getenv("AI_API_BASE_URL", "https://example.com").rstrip("/")
MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

MIN_INTENT_SIMILARITY = float(os.getenv("MIN_INTENT_SIMILARITY", "0.75"))
MIN_REPLY_SIMILARITY = float(os.getenv("MIN_REPLY_SIMILARITY", "0.78"))
