project:
  name: "AI Conversation API – API-Only Automation Framework"
  description: >
    An API-only automation framework for validating AI Conversation APIs.
    The framework focuses on semantic quality validation in addition to
    standard API contract checks.

use_case:
  overview:
    - Create a conversation session
    - Send a user message to the conversation
    - Validate AI-generated response quality
  validations:
    api_contract:
      - conversationId
      - userMessage
    semantic_quality:
      method: cosine_similarity
      scope:
        - intent recognition
        - AI reply content
    confidence_rule:
      description: >
        Confidence score returned by the API must be greater than or equal
        to the average semantic similarity score.
      rule: "confidence >= average_similarity"

architecture:
  pattern: service_layer
  components:
    tests:
      responsibility: "Test orchestration and assertions"
    services:
      responsibility: "Workflow orchestration (conversation lifecycle)"
    clients:
      responsibility: "API and embeddings clients (mock and real)"
    validators:
      responsibility: "Semantic scoring and quality rules"
    utils:
      responsibility: "CSV loader and logging utilities"
    data:
      responsibility: "CSV-driven test cases"

test_data:
  source: "data/test_cases.csv"
  required_columns:
    - conversation_id
    - user_id
    - channel
    - expected_user_message
    - expected_intent
    - language
  optional_columns:
    - expected_ai_reply
  notes: "expected_ai_reply is recommended for semantic reply validation"

mock_mode:
  enabled_by_default: true
  base_url: "https://example.com"
  description: >
    Mock mode returns seeded responses so the entire automation flow
    runs end-to-end without a live API.
  real_environment:
    steps:
      - set MOCK_MODE=false
      - update AI_API_BASE_URL to deployed domain

setup:
  environment_configuration:
    steps:
      - "cp .env.example .env"
    offline_execution:
      recommended: true
      variables:
        EMBEDDINGS_PROVIDER: "sklearn"
        MOCK_MODE: true
    openai_execution:
      variables:
        EMBEDDINGS_PROVIDER: "openai"
        OPENAI_API_KEY: "<your_openai_api_key>"
        OPENAI_EMBEDDING_MODEL: "text-embedding-3-small"
      note: >
        ChatGPT Plus is separate from OpenAI API billing.
        If API quota is unavailable, use sklearn embeddings.
  virtual_environment:
    create:
      command: "python3 -m venv .venv"
    activate:
      command: "source .venv/bin/activate"
    verify:
      command: "python --version"
  dependencies:
    install:
      - "python -m pip install -U pip"
      - "python -m pip install -e ."

execution:
  run_all_tests:
    command: "pytest -s"
    description:
      - CSV-driven test execution
      - Service-layer orchestration
      - Mock API client usage
      - Semantic validation (intent + reply)
      - Confidence vs similarity enforcement

reporting:
  html_report:
    generate:
      commands:
        - "mkdir -p reports"
        - "pytest -s --html=reports/report.html --self-contained-html"
    open_mac:
      command: "open reports/report.html"
    contents:
      - test execution results
      - captured logs
      - semantic validation output
      - assertion failures (if any)

logging:
  approach: structured_logging
  layers:
    - services
    - validators
  logged_steps:
    - conversation creation
    - message submission
    - AI reply receipt
    - intent, confidence, and similarity scores
  visibility:
    - terminal output
    - HTML report capture

test_coverage:
  types:
    - end_to_end_semantic_validation
    - api_contract_validation
    - positive_semantic_quality_tests
    - negative_quality_guardrail_tests

extensibility:
  capabilities:
    - add_new_embedding_providers
    - add_additional_semantic_rules
    - extend_csv_with_more_scenarios
    - switch_from_mock_to_real_api
    - integrate_with_ci_cd_pipelines

summary:
  highlights:
    - API-only automation
    - Service layer architecture
    - Semantic similarity scoring
    - Confidence-based quality enforcement
    - Scalable, CSV-driven testing
