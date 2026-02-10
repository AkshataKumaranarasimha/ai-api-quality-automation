from sklearn.feature_extraction.text import TfidfVectorizer

class SklearnEmbeddingsClient:
    """
    Local embeddings client using TF-IDF vectors.
    NOTE: For intent labels, we normalize underscores/hyphens into spaces.
    """

    def __init__(self):
        self._vectorizer = TfidfVectorizer()

    @staticmethod
    def _normalize(text: str) -> str:
        # Makes label-like strings comparable:
        # INSURANCE_OFFERS -> "insurance offers"
        return (
            str(text)
            .replace("_", " ")
            .replace("-", " ")
            .strip()
            .lower()
        )

    def embed_pair(self, text_a: str, text_b: str) -> tuple[list[float], list[float]]:
        a = self._normalize(text_a)
        b = self._normalize(text_b)

        matrix = self._vectorizer.fit_transform([a, b]).toarray()
        return matrix[0].tolist(), matrix[1].tolist()

'''
if __name__ == "__main__":
    from src.clients.sklearn_embeddings_client import SklearnEmbeddingsClient

    emb = SklearnEmbeddingsClient()
    validator = SemanticQualityValidator()

    expected_intent = "GET_VEHICLE_INSURANCE_OFFERS"
    actual_intent = "INSURANCE_OFFERS"

    # Debug: print the vectors used for intent
    v1, v2 = emb.embed_pair(expected_intent, actual_intent)
    print("\n[DEBUG] Intent vectors")
    print("v1:", v1)
    print("v2:", v2)

    intent_sim = validator._cos_sim(v1, v2)
    print("[DEBUG] Intent similarity (direct):", intent_sim)

    scores = validator.validate(
        emb_client=emb,
        expected_intent=expected_intent,
        actual_intent=actual_intent,
        expected_reply="I can help with vehicle insurance offers.",
        actual_reply="I can help with insurance offers for your vehicle.",
        confidence=0.93,
    )

    print("\n[VALIDATOR SANITY CHECK]")
    print(scores)

'''