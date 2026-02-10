import pytest
from src.utils.csv_loader import load_csv_test_cases


TEST_CASES = load_csv_test_cases("data/test_cases.csv")


def _get_case(conversation_id: str) -> dict:
    for row in TEST_CASES:
        if row["conversation_id"] == conversation_id:
            return row
    raise ValueError(f"Test case not found in CSV: {conversation_id}")


def test_conversation_id_is_returned(service):
    """
    Minimal check: conversationId exists and is non-empty.
    """
    row = _get_case("conv-seed-001")

    resp = service.start_and_send(
        user_id=row["user_id"],
        channel=row["channel"],
        user_message=row["expected_user_message"],
        language=row["language"],
    )

    assert isinstance(resp.conversationId, str)
    assert resp.conversationId.strip() != ""


def test_response_contract_fields(service):
    """
    Contract check: response has required fields + metadata fields.
    """
    row = _get_case("conv-seed-001")

    resp = service.start_and_send(
        user_id=row["user_id"],
        channel=row["channel"],
        user_message=row["expected_user_message"],
        language=row["language"],
    )

    # Top-level fields
    assert resp.conversationId
    assert resp.userMessage
    assert resp.aiReply

    # Metadata fields
    assert resp.metadata.intent
    assert 0.0 <= resp.metadata.confidence <= 1.0


def test_end_to_end_semantic_quality_positive(service, emb_client, validator):
    """
    End-to-end: CSV -> Service -> Mock API -> Semantic Validator.
    This should PASS.
    """
    row = _get_case("conv-seed-001")

    resp = service.start_and_send(
        user_id=row["user_id"],
        channel=row["channel"],
        user_message=row["expected_user_message"],
        language=row["language"],
    )

    scores = validator.validate(
        emb_client=emb_client,
        expected_intent=row["expected_intent"],
        actual_intent=resp.metadata.intent,
        expected_reply=row["expected_ai_reply"],
        actual_reply=resp.aiReply,
        confidence=resp.metadata.confidence,
    )

    # Optional: basic sanity asserts so you see values are produced
    assert scores.avg_similarity >= 0.0


def test_semantic_quality_negative_should_fail(service, emb_client, validator):
    """
    Negative test: intentionally wrong expectations to prove the validator fails.
    """
    row = _get_case("conv-seed-001")

    resp = service.start_and_send(
        user_id=row["user_id"],
        channel=row["channel"],
        user_message=row["expected_user_message"],
        language=row["language"],
    )

    # Force an obviously incorrect expected intent/reply
    wrong_expected_intent = "CANCEL_APPOINTMENT"
    wrong_expected_reply = "Your payment has been processed successfully."

    with pytest.raises(AssertionError):
        validator.validate(
            emb_client=emb_client,
            expected_intent=wrong_expected_intent,
            actual_intent=resp.metadata.intent,
            expected_reply=wrong_expected_reply,
            actual_reply=resp.aiReply,
            confidence=resp.metadata.confidence,
        )
