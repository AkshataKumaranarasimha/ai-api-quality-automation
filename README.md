# AI Conversation API – API-Only Automation Framework (Service Layer)

This project demonstrates an API-only automation framework for an AI Conversation API where a user message triggers an AI reply.

## Use case
- Create a conversation session
- Send a user message to the conversation
- Validate:
  - API contract and deterministic fields (conversationId, userMessage)
  - Semantic quality using OpenAI embeddings + cosine similarity
  - Intent recognition quality
  - Confidence quality (confidence must be >= average semantic similarity score)

## Architecture
Service layer pattern for scalability:
- `tests/` call `services/`
- `services/` orchestrate workflow across `clients/`
- `clients/` handle HTTP calls (supports mock mode)
- `validators/` handle semantic scoring and quality rules
- `data/` provides CSV-driven test cases

## Test data (CSV)
The suite reads test cases from `data/test_cases.csv`.
Required columns:
- `conversation_id`
- `user_id`
- `channel`
- `expected_user_message`
- `expected_intent`
- `language` (default: `en-US`)

Optional columns:
- `expected_ai_reply` (recommended for semantic reply validation)

## Mock mode (default)
There is no live API implementation required.
By default, `AI_API_BASE_URL=https://example.com` and `MOCK_MODE=true`.
In mock mode, the API client returns seeded responses so the full automation flow runs end-to-end.

To run against a real environment later:
- Set `MOCK_MODE=false`
- Update `AI_API_BASE_URL` to your deployed domain

## Setup

### 1) Configure environment
```bash
cp .env.example .env
# Add OPENAI_API_KEY in .env
