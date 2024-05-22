"""
This module contains the implementation of the LDA class,
which applies Latent Dirichlet Allocation (LDA) to a corpus of documents and extracts topics.

Classes:
- LDA: A class to apply LDA to a corpus of documents and extract topics.
"""

from gensim.corpora import Dictionary
from gensim.models import CoherenceModel
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer


class LDA:
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
        self.coherence: float = float('inf')
        self.topics: list[list[str]] = []
        self.topic_distributions: list[dict[str, float]] = []
        self.vectorizer: CountVectorizer = CountVectorizer()
        self.model: LatentDirichletAllocation = LatentDirichletAllocation(
            n_components=num_topics, random_state=0
        )

    def fit(self) -> None:
        """
        Fit the LDA model to the corpus of documents and extract the top words for each topic.
        """
        X = self.vectorizer.fit_transform(self.corpus)
        self.vectorizer.get_feature_names_out()
        self.model = LatentDirichletAllocation(
            n_components=self.num_topics, random_state=0
        )

        self.model.fit(X)
        self.topics = self.__get_topics()

    def predict(self, doc: str) -> dict[int, float]:
        """
        Predict the topic distribution for a new document.

        Args:
        - doc (str): The new document.

        Returns:
        - list[float]: The topic distribution for the new document.
        """
        dists: dict[int, float] = {}
        X = self.vectorizer.transform([doc])
        for i, dist in enumerate(self.model.transform(X)[0]):
            dists[i] = dist

        return dists

    def predict_all(self) -> None:
        """
        Predict the topic distribution for all documents in the corpus.

        The results are available in `LDA.topic_distributions`
        """
        self.topic_distributions = [self.predict(doc) for doc in self.corpus]

    def calculate_coherence(self) -> None:
        """
        Calculate the coherence of the topics.

        The result is available in `LDA.coherence`
        """
        texts = [doc.split() for doc in self.corpus]
        dictionary = Dictionary(texts)

        coherence_model = CoherenceModel(
            model=self.model,
            texts=texts,
            dictionary=dictionary,
            coherence='c_v',
            topics=self.__get_topics(),
        )
        self.coherence = coherence_model.get_coherence()

    def __get_topics(self) -> list[list[str]]:
        """
        Get the top words for each topic in the LDA model.

        Returns:
        - list[list[str]]: The top words for each topic.
        """
        vocab = self.vectorizer.get_feature_names_out()
        topics = []
        for topic in self.model.components_:
            topics.append(
                [vocab[i] for i in topic.argsort()[: -self.num_words - 1: -1]]
            )
        return topics
