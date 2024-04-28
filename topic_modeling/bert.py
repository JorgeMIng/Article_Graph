"""
This module contains the implementation of the BERT class,
which applies BERTopic to a corpus of documents and extracts topics.

Classes:
- BERT: A class to apply BERTopic to a corpus of documents and extract topics.
"""

from bertopic import BERTopic


class BERT:
    """
    A class to apply BERTopic to a corpus of documents and extract topics.
    """

    def __init__(self, corpus: list[str], num_words: int = 5):
        self.corpus: list[str] = corpus
        self.num_words: int = num_words
        self.topics: list[int] = []
        self.probs: list[int] = []
        self.model: BERTopic = BERTopic(
            language='multilingual',
            top_n_words=num_words
        )

    def fit(self):
        """
        Fit the BERTopic model to the corpus of documents and extract the topics.
        """

    def predict(self, doc: str) -> list[float]:
        """
        Predict the topic distribution for a new document.
        """

    def __get_topics(self, n_words: int = 5) -> list[list[str]]:
        """
        Get the top words for each topic.
        """
