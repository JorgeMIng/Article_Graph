# pip install -U sentence-transformers
# all-MiniLM-L6-v2

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class MiniLM:
    def __init__(self, texts):
        # Initialize the MiniLM class with a list of texts
        self.texts = texts
        # Initialize the SentenceTransformer model
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    def calculate_similarity(self):
        # Calculate embeddings for the texts
        embeddings = self.model.encode(self.texts)

        # Calculate cosine similarity between all pairs of texts
        similarity_scores = cosine_similarity(embeddings)

        # Create a list to store similarity results
        similarity_results = []

        # Fill the list with similarity results
        for i in range(len(self.texts)):
            for j in range(i+1, len(self.texts)):
                # Each element of the list is a dictionary containing similarity information
                result = {'text_id1': i, 'text_id2': j, 'similarity': similarity_scores[i][j]}
                similarity_results.append(result)

        # Print similarity results
        print("Similarity results:")
        for result in similarity_results:
            print(result)