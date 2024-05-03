from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class Model:
    def __init__(self, texts, model_name):
        """
        Initialize the class.

        Args:
        texts (list): List of texts to be used for similarity calculation.
        model_name (str): Name of the SentenceTransformer model to use.
        """
        # Initialize the texts
        self.texts = texts

        # Initialize the SentenceTransformer model
        self.model = SentenceTransformer(model_name)

    def calculate_similarity(self):
        """
        Calculate the cosine similarity between all pairs of texts.
        """
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