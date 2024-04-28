"""
This module contains the implementation of the LDATopicModel class,
which applies Latent Dirichlet Allocation (LDA) to a corpus of documents and extracts topics.

Classes:
- LDATopicModel: A class to apply LDA to a corpus of documents and extract topics.
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from gensim.corpora import Dictionary
from gensim.models import CoherenceModel


class LDATopicModel():
    """
    A class to apply Latent Dirichlet Allocation (LDA) to a corpus of documents and extract topics.
    """

    def __init__(self, corpus: list[str], num_topics: int = 3, num_words: int = 5):
        """
        Initialize the LDA topic model with the given corpus of documents and number of topics.

        Args:
        - corpus (list[str]): The corpus of documents.
        - num_topics (int): The number of topics to extract. Default is 3.
        - num_words (int): The number of words to include in each topic. Default is 5.
        """
        self.corpus: list[str] = corpus
        self.num_topics: int = num_topics
        self.num_words: int = num_words
        self.vectorizer: CountVectorizer = None
        self.model: LatentDirichletAllocation = None
        self.topics: list[list[str]] = None
        self.probs: list[float] = None

    def fit(self):
        """
        Fit the LDA model to the corpus of documents and extract the top words for each topic.
        """
        self.vectorizer = CountVectorizer()
        matrix = self.vectorizer.fit_transform(self.corpus)

        self.vectorizer.get_feature_names_out()

        self.model = LatentDirichletAllocation(
            n_components=self.num_topics,
            random_state=0
        )

        self.model.fit(matrix)

        self.topics = self.__get_topics()

    def predict(self, doc: str) -> list[float]:
        """
        Predict the topic distribution for a new document.

        Args:
        - doc (str): The new document.

        Returns:
        - list[float]: The topic distribution for the new document.
        """
        matrix = self.vectorizer.transform([doc])
        self.probs = self.model.transform(matrix)[0]

    def calculate_coherence(self) -> float:
        """
        Calculate the coherence of the topics.
        """
        coherence_model = CoherenceModel(
            topics=self.topics,
            texts=[self.vectorizer.get_feature_names_out()],
            dictionary=Dictionary([self.vectorizer.get_feature_names_out()]),
            coherence='c_npmi'
        )
        return coherence_model.get_coherence()

    def __get_topics(self) -> list[list[str]]:
        """
        Get the top words for each topic in the LDA model.

        Returns:
        - list[list[str]]: The top words for each topic.
        """
        vocab = self.vectorizer.get_feature_names_out()
        topics = []
        for topic in self.model.components_:
            topics.append([vocab[i]
                          for i in topic.argsort()[:-self.num_words-1:-1]])
        return topics
