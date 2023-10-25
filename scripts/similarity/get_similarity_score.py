import json
import logging
import os
import numpy as np
from gensim.models import Word2Vec
import faiss


logging.basicConfig(
    filename='app_similarity_score.log',
    filemode='w',
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("app_similarity_score.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def train_word2vec(data):
    # Train a Word2Vec model on the provided data.
    model = Word2Vec(sentences=data, vector_size=100, window=5, min_count=1, sg=1)
    model.save("word2vec.model")

def get_embedding(text, model):
    try:
        embeddings = [model.wv[word] for word in text.split() if word in model.wv]
        if not embeddings:
            return None
        return embeddings[0]
    except Exception as e:
        logger.error(f"Error getting embeddings: {e}", exc_info=True)

class SimilarityScorer:
    def __init__(self, resumes, jd):
        self.resumes = resumes
        self.jd = jd
        self.logger = logging.getLogger(self.__class__.__name__)
        self.train_word2vec(resumes)

    def search(self):
        # Load the Word2Vec model
        model = Word2Vec.load("word2vec.model")

        # Create a Faiss index and normalize vectors
        index = faiss.IndexFlatL2(100)
        vectors = [get_embedding(resume, model) for resume in self.resumes]
        vectors = [vector for vector in vectors if vector is not None]
        faiss_vectors = np.array(vectors, dtype=np.float32)
        faiss.normalize_L2(faiss_vectors)
        index.add(faiss_vectors)

        # Query the index with the job description vector
        jd_vector = get_embedding(self.jd, model)
        if jd_vector is not None:
            faiss.normalize_L2(jd_vector)
            D, I = index.search(np.array([jd_vector], dtype=np.float32), 30)

            results = []
            for i, idx in enumerate(I[0]):
                result = {
                    'text': self.resumes[idx][:30],
                    'score': 1 / (1 + D[0][i])
                }
                results.append(result)
            return results
        else:
            return []

# Example usage
if __name__ == "__main__":
    # Load your resumes and job description data
    resumes = ["resume_text_1", "resume_text_2", "resume_text_3"]
    job_description = "job_description_text"

    similarity_scorer = SimilarityScorer(resumes, job_description)
    results = similarity_scorer.search()
    for r in results:
        print(r)