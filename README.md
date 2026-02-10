# AI Conversation API – API-Only Automation Framework

API-only automation framework for validating AI Conversation APIs with semantic quality checks.

---

## What This Covers

- Create conversation sessions
- Send user messages
- Validate:
  - API contract fields
  - Intent recognition
  - AI reply semantic similarity (cosine similarity)
  - Confidence ≥ average semantic similarity score

---

## Architecture

Service-layer based design:

- `tests/` – test cases and assertions  
- `services/` – workflow orchestration  
- `clients/` – API and embeddings clients (mock + real)  
- `validators/` – semantic validation logic  
- `data/` – CSV-driven test cases  

---

## Test Data

CSV file:
data/test_cases.csv


Required columns:
- `conversation_id`
- `user_id`
- `channel`
- `expected_user_message`
- `expected_intent`
- `language`

Optional:
- `expected_ai_reply`

---

## Setup

```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
Embeddings Provider
Default (offline):

EMBEDDINGS_PROVIDER=sklearn
OpenAI (requires API key + quota):

EMBEDDINGS_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
Run Tests
pytest -s
HTML Report
mkdir -p reports
pytest -s --html=reports/report.html --self-contained-html
open reports/report.html
Logging
Structured logs at service and validator layers

Visible in terminal and captured in HTML report
```
##Summary

- `API-only testing`
- `Service-layer architecture`
- `Semantic validation using embeddings`
- `CSV-driven and scalable`
