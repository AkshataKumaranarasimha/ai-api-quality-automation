from pydantic import BaseModel, Field
from typing import Literal, Optional

class CreateConversationRequest(BaseModel):
    userId: str
    channel: Literal["voice", "chat"]

class CreateConversationResponse(BaseModel):
    conversationId: str = Field(min_length=1)

class MessageRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    language: str = Field(min_length=2)

class Metadata(BaseModel):
    intent: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)

class MessageResponse(BaseModel):
    conversationId: str
    userMessage: str
    aiReply: str
    metadata: Metadata
'''
if __name__ == "__main__":
    print("\n=== SCHEMA SANITY CHECKS ===")
    # Case 1: VALID response (should PASS)
    print(" Case 1: Valid response payload")

    valid_payload = {
        "conversationId": "conv-seed-001",
        "userMessage": "I want to reschedule my appointment",
        "aiReply": "Sure — I can help you reschedule your appointment.",
        "metadata": {
            "intent": "RESCHEDULE_APPOINTMENT",
            "confidence": 0.92
        }
    }

    try:
        parsed = MessageResponse.model_validate(valid_payload)
        print("PASS: Valid response accepted by schema")
        print(parsed.model_dump())
    except Exception as e:
        print("FAIL (unexpected):", e)

    # Case 2: INVALID response (should FAIL)
    # Missing aiReply + confidence out of range

    print("\n[CASE 2] Invalid response payload")

    invalid_payload = {
        "conversationId": "conv-seed-002",
        "userMessage": "My vehicle insurance is expired",
        # aiReply is missing
        "metadata": {
            "intent": "INSURANCE_OFFERS",
            "confidence": 1.5   # invalid (> 1.0)
        }
    }

    try:
        MessageResponse.model_validate(invalid_payload)
        print("FAIL: Invalid response was incorrectly accepted")
    except Exception as e:
        print("PASS: Invalid response correctly rejected")
        print("Error:", e)

'''

