from typing import List, Dict, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

import config
from data_loader import ConversationDataset


class HybridRetriever:
    def __init__(self, dataset: ConversationDataset):
        print("=" * 60)
        print("INITIALIZING HYBRID RETRIEVER")
        print("=" * 60)

        self.dataset = dataset
        self.conversations = dataset.get_all_conversations()
        print("Preparing documents...")
        self.doc_ids, self.documents = self._prepare_documents()
        print("Building TF-IDF index...")
        self.tfidf = TfidfVectorizer(
            max_features=50000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.tfidf_matrix = self.tfidf.fit_transform(self.documents)
        print("Loading embedding model...")
        self.embedder = SentenceTransformer(config.EMBEDDING_MODEL)

        print("Encoding documents (this may take a few minutes)...")
        self.embeddings = self.embedder.encode(
            self.documents,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        print("✓ Hybrid Retriever Ready")
        print("=" * 60)

    def _prepare_documents(self) -> Tuple[List[str], List[str]]:
        doc_ids = []
        documents = []

        for conv in self.conversations:
            texts = []
            texts.append(f"Domain: {conv['domain']}")
            texts.append(f"Intent: {conv['intent']}")
            texts.append(f"Reason: {conv['reason_for_call']}")
            for turn in conv['conversation']:
                texts.append(f"{turn['speaker']}: {turn['text']}")

            full_text = " ".join(texts)

            doc_ids.append(conv['transcript_id'])
            documents.append(full_text)

        return doc_ids, documents

    def search(self, query: str, top_k: int = None) -> List[Dict]:
        if top_k is None:
            top_k = config.TOP_K_RETRIEVE
        query_vec = self.tfidf.transform([query])
        tfidf_scores = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        query_emb = self.embedder.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        semantic_scores = cosine_similarity(query_emb, self.embeddings)[0]
        final_scores = (
            config.KEYWORD_WEIGHT * tfidf_scores +
            config.SEMANTIC_WEIGHT * semantic_scores
        )
        top_indices = np.argsort(final_scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "transcript_id": self.doc_ids[idx],
                "score": float(final_scores[idx]),
                "semantic_score": float(semantic_scores[idx]),
                "keyword_score": float(tfidf_scores[idx])
            })

        return results


# =========================
# TESTING
# =========================
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TESTING HYBRID RETRIEVER")
    print("=" * 60)

    dataset = ConversationDataset()
    retriever = HybridRetriever(dataset)

    test_query = (
        "customer repeatedly contacted support but issue was not resolved "
        "and asked for a supervisor"
    )

    print(f"\nQuery: {test_query}")
    results = retriever.search(test_query, top_k=6)

    print("\nTop Results:")
    for i, res in enumerate(results, 1):
        conv = dataset.get_conversation(res["transcript_id"])
        print(f"\n{i}. Call ID: {res['transcript_id']}")
        print(f"   Score: {res['score']:.4f}")
        print(f"   Domain: {conv['domain']}")
        print(f"   Intent: {conv['intent']}")
        print(f"   Reason: {conv['reason_for_call'][:120]}...")
