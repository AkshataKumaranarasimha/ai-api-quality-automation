from sklearn.feature_extraction.text import TfidfVectorizer

class SklearnEmbeddingsClient:
    """
    Local embeddings client using TF-IDF vectors.
    - No network calls
    - Works in CI/offline
    - Good for demo flows when OpenAI API is unavailable
    """

    def __init__(self):
        # We'll fit on the pair (expected, actual) per comparison, so no global fit needed.
        self._vectorizer = TfidfVectorizer()

    def embed_pair(self, text_a: str, text_b: str) -> tuple[list[float], list[float]]:
        """
        TF-IDF needs a shared vocabulary to compare texts properly.
        So we fit on [text_a, text_b] and return vectors for both.
        """
        matrix = self._vectorizer.fit_transform([text_a, text_b]).toarray()
        return matrix[0].tolist(), matrix[1].tolist()


'''
if __name__ == "__main__":
    client = SklearnEmbeddingsClient()
    a, b = client.embed_pair("GET_VEHICLE_INSURANCE_OFFERS", "INSURANCE_OFFERS")
    print("\n[SKLEARN EMBEDDING SANITY CHECK]")
    print("Vector length:", len(a))
    print("First 5 a:", a[:5])
    print("First 5 b:", b[:5])
'''