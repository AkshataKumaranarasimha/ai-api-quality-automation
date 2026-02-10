import pytest
import sys
from pathlib import Path
from src.clients.conversation_api_client import ConversationApiClient
from src.clients.embeddings_factor import get_embeddings_client
from src.services.conversation_service import ConversationService
from src.validators.semantic_quality_validator import SemanticQualityValidator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

@pytest.fixture(scope="session")
def api_client():
    # Use mock API client for all tests to avoid external dependencies
    return ConversationApiClient(mock_mode=True)

@pytest.fixture(scope="session")
def service(api_client):
    # Service layer that uses the API client
    return ConversationService(api_client)

@pytest.fixture(scope="session")
def emb_client():
    # Embeddings client (sklearn or OpenAI based on env var)
    return get_embeddings_client()

@pytest.fixture(scope="session")
def validator():
    # Semantic quality validator instance
    return SemanticQualityValidator()