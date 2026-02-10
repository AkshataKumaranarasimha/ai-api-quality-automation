from dataclasses import dataclass
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class SimilarityScores:
    intent_similarity: float
    reply_similarity: float
    avg_similarity: float


class SemanticQualityValidator:
    """
    Computes semantic similarity for:
      - intent (expected vs actual)
      - reply (expected vs actual)

    Rule enforced:
      confidence >= average(intent_similarity, reply_similarity)

    Works with:
      - SklearnEmbeddingsClient (embed_pair)
      - OpenAIEmbeddingsClient (embed)
    """

    @staticmethod
    def _cos_sim(vec_a: list[float], vec_b: list[float]) -> float:
        return float(cosine_similarity([vec_a], [vec_b])[0][0])

    def _get_vectors(self, emb_client, text_a: str, text_b: str):
        if hasattr(emb_client, "embed_pair"):
            return emb_client.embed_pair(text_a, text_b)

        return emb_client.embed(text_a), emb_client.embed(text_b)

    def validate(
        self,
        emb_client,
        expected_intent: str,
        actual_intent: str,
        expected_reply: str,
        actual_reply: str,
        confidence: float,
    ) -> SimilarityScores:

        v_exp_int, v_act_int = self._get_vectors(emb_client, expected_intent, actual_intent)
        intent_sim = self._cos_sim(v_exp_int, v_act_int)

        v_exp_rep, v_act_rep = self._get_vectors(emb_client, expected_reply, actual_reply)
        reply_sim = self._cos_sim(v_exp_rep, v_act_rep)

        avg_sim = (intent_sim + reply_sim) / 2.0

        assert confidence >= avg_sim, (
            f"Confidence {confidence:.3f} must be >= avg similarity {avg_sim:.3f} "
            f"(intent={intent_sim:.3f}, reply={reply_sim:.3f})"
        )

        return SimilarityScores(
            intent_similarity=intent_sim,
            reply_similarity=reply_sim,
            avg_similarity=avg_sim,
        )


# Local sanity check
if __name__ == "__main__":
    from src.clients.sklearn_embeddings_client import SklearnEmbeddingsClient

    emb = SklearnEmbeddingsClient()
    validator = SemanticQualityValidator()

    scores = validator.validate(
        emb_client=emb,
        expected_intent="GET_VEHICLE_INSURANCE_OFFERS",
        actual_intent="INSURANCE_OFFERS",
        expected_reply="I can help with vehicle insurance offers.",
        actual_reply="I can help with insurance offers for your vehicle.",
        confidence=0.93,
    )

    print("\n[VALIDATOR SANITY CHECK]")
    print(scores)
