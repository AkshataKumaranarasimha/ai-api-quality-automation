from src.clients.conversation_api_client import ConversationApiClient
from src.models.schemas import CreateConversationRequest, MessageRequest, MessageResponse

class ConversationService:
    """
    Service layer:
    - Orchestrates multi-step workflows
    - Keeps tests clean and scalable
    """

    def __init__(self, api_client: ConversationApiClient):
        self.api_client = api_client

    def start_conversation(self, user_id: str, channel: str):
        # Calls the API client to create a conversation session
        return self.api_client.create_conversation(
            CreateConversationRequest(userId=user_id, channel=channel)
        )

    def send_user_message(self, conversation_id: str, user_message: str, language: str) -> MessageResponse:
        # Calls the API client to send a message and receive AI reply + metadata
        return self.api_client.send_message(
            conversation_id=conversation_id,
            payload=MessageRequest(message=user_message, language=language)
        )

    def start_and_send(self, user_id: str, channel: str, user_message: str, language: str) -> MessageResponse:
        # Orchestrates: create conversation -> send message
        conv = self.start_conversation(user_id=user_id, channel=channel)
        return self.send_user_message(
            conversation_id=conv.conversationId,
            user_message=user_message,
            language=language
        )


'''
if __name__ == "__main__":
    client = ConversationApiClient(mock_mode=True)
    service = ConversationService(client)

    # Case: insurance
    resp = service.start_and_send(
        user_id="user-456",
        channel="voice",
        user_message="My vehicle insurance is expired. Could you please help me out?",
        language="en-US"
    )

    print("\n[SERVICE LAYER OUTPUT]")
    print(resp.model_dump())
'''