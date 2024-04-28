"""
This module contains the implementation of the BERTopicModel class,
which applies BERTopic to a corpus of documents and extracts topics.

Classes:
- BERTopicModel: A class to apply BERTopic to a corpus of documents and extract topics.
"""

from bertopic import BERTopic


class BERTopicModel:
    """
    A class to apply BERTopic to a corpus of documents and extract topics.
    """

    def __init__(self, corpus: list[str], n_words: int = 5):
        self.corpus: list[str] = corpus
        self.n_words: int = n_words
        self.model: BERTopic = None
        self.topics: list[int] = None

    def fit(self):
        """
        Fit the BERTopic model to the corpus of documents and extract the topics.
        """
        self.model = BERTopic(language='multilingual',
                              top_n_words=self.n_words)

        self.topics, self.probs = self.model.fit_transform(self.corpus)

    def predict(self, doc: str) -> list[float]:
        """
        Predict the topic distribution for a new document.
        """
        return self.model.transform([doc])[0]

    def __get_topics(self, n_words: int = 5) -> list[list[str]]:
        """
        Get the top words for each topic.
        """
        return self.model.get_topics(n_words=n_words)
