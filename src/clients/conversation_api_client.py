import httpx
from pathlib import Path

from src.models.schemas import (
    CreateConversationRequest,
    CreateConversationResponse,
    MessageRequest,
    MessageResponse,
)

class ConversationApiClient:
    """
    API Client for:
      - POST /ai/conversations
      - POST /ai/conversations/{conversationId}/message

    For now, we run in MOCK mode (seeded responses) so the framework runs end-to-end
    even without a real API implementation.
    """

    def __init__(self, base_url: str = "https://example.com", mock_mode: bool = True):
        self.base_url = base_url.rstrip("/")
        self.mock_mode = mock_mode

    def create_conversation(self, payload: CreateConversationRequest) -> CreateConversationResponse:
        # This method is executed to create a conversation session.
        if self.mock_mode:
            # Seeded conversation ID for demo; stable + predictable.
            return CreateConversationResponse(conversationId="conv-seed-001")

        url = f"{self.base_url}/ai/conversations"
        r = httpx.post(url, json=payload.model_dump(), timeout=30)
        r.raise_for_status()
        return CreateConversationResponse.model_validate(r.json())

    def send_message(self, conversation_id: str, payload: MessageRequest) -> MessageResponse:
        # This method is executed to send a user message and receive AI reply + metadata.
        if self.mock_mode:
            msg = payload.message.lower()

            # Default: reschedule scenario
            intent = "RESCHEDULE_APPOINTMENT"
            ai_reply = "Sure — I can help you reschedule your appointment. What date and time would you prefer?"
            confidence = 0.92

            # Use case: insurance expired -> API returns INSURANCE_OFFERS (expected may be GET_VEHICLE_INSURANCE_OFFERS)
            if "insurance" in msg and ("vehicle" in msg or "car" in msg) and ("expired" in msg or "renew" in msg):
                intent = "INSURANCE_OFFERS"
                ai_reply = (
                    "I can help with insurance offers. Please share your vehicle type, location, "
                    "and preferred coverage so I can show suitable options."
                )
                confidence = 0.93

            seeded = {
                "conversationId": conversation_id,
                "userMessage": payload.message,
                "aiReply": ai_reply,
                "metadata": {"intent": intent, "confidence": confidence},
            }

            print("\n[MOCK API RESPONSE]")
            print(seeded)

            return MessageResponse.model_validate(seeded)

        url = f"{self.base_url}/ai/conversations/{conversation_id}/message"
        r = httpx.post(url, json=payload.model_dump(), timeout=60)
        r.raise_for_status()
        return MessageResponse.model_validate(r.json())


'''
if __name__ == "__main__":
    client = ConversationApiClient(mock_mode=True)

    # Case 1: reschedule
    conv = client.create_conversation(CreateConversationRequest(userId="user-123", channel="voice"))
    resp1 = client.send_message(conv.conversationId, MessageRequest(
        message="I want to reschedule my appointment",
        language="en-US"
    ))
    print("\nParsed Response 1:\n", resp1.model_dump())

    # Case 2: insurance
    conv2 = CreateConversationResponse(conversationId="conv-seed-002")
    resp2 = client.send_message(conv2.conversationId, MessageRequest(
        message="My vehicle insurance is expired. Could you please help me out?",
        language="en-US"
    ))
    print("\nParsed Response 2:\n", resp2.model_dump())
'''