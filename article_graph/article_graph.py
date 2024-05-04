"""
This module contains the class responsible for building an RDF graph.
"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, XSD
from ._utils import xml_date_to_xsd_date


class ArticleGraph:
    """
    This class is responsible for building an RDF graph.
    """

    def __init__(self) -> None:
        """
        Initialize the graph.
        """
        self.graph = Graph()
        self.ns = Namespace('http://open_science.com/')

    def add_paper(self, paper_id: int, title: str, abstract: str, release_date: str | None = None):
        """
        Add a paper to the graph.
        """
        paper_node = self.ns[f'paper#{paper_id}']

        # Add the type, label, title and abstract of the Paper node
        self.graph.add((paper_node, RDF.type, self.ns.Paper))
        self.graph.add((paper_node, RDFS.label, Literal(f'paper-{paper_id}')))
        self.graph.add((paper_node, self.ns['title'], Literal(title)))
        self.graph.add((paper_node, self.ns['abstract'], Literal(abstract)))

        # Add the release_date if provided
        if release_date is not None:
            self.graph.add(
                (paper_node,
                 self.ns['release_date'],
                 Literal(xml_date_to_xsd_date(release_date), datatype=XSD.date)))

    def add_topic(self, topic_id: int, keywords: list[str]):
        """
        Add a topic to the graph.
        """
        topic_node = self.ns[f'topic#{topic_id}']

        # Add the type and the label of the Topic node
        self.graph.add((topic_node, RDF.type, self.ns.Topic))
        self.graph.add((topic_node, RDFS.label, Literal(f'topic-{topic_id}')))

        # Add all the keywords to the Topic node
        for kw in keywords:
            self.graph.add((topic_node, self.ns['keyword'], Literal(kw)))

    def add_topic_belonging(self, paper_id: int, topic_id: int, degree: float):
        """
        Add a topic belonging relationship to the graph.
        """
        topic_belonging_fragment = f'topic_belonging#{paper_id}{topic_id}'
        topic_belonging_node = self.ns[topic_belonging_fragment]
        paper_node = self.ns[f'paper#{paper_id}']
        topic_node = self.ns[f'topic#{topic_id}']

        # Add the type, label and degree of the TopicBelonging node
        self.graph.add(
            (topic_belonging_node, RDF.type, self.ns.TopicBelonging))
        self.graph.add(
            (topic_belonging_node, RDFS.label, Literal(topic_belonging_fragment)))
        self.graph.add(
            (topic_belonging_node, self.ns['degree'], Literal(degree, datatype=XSD.float)))

        # Add the belongs_to_topic of the Paper node
        self.graph.add(
            (paper_node, self.ns['belongs_to_topic'], topic_belonging_node))

        # Add the topic of the Topic node
        self.graph.add(
            (topic_belonging_node, self.ns['topic'], topic_node))
        
    def add_similarity(self, text_id1: int, text_id2: int, similarity_score: float):
        """
        Add similarity between two texts to the graph.
        """
        similarity_node = self.ns[f'similarity#{text_id1}-{text_id2}']

        # Add the type, label, and similarity score of the Similarity node
        self.graph.add((similarity_node, RDF.type, self.ns.Similarity))
        self.graph.add((similarity_node, RDFS.label, Literal(f'similarity-{text_id1}-{text_id2}')))
        self.graph.add((similarity_node, self.ns['degree'], Literal(similarity_score, datatype=XSD.float)))

        # Connect similarity to paper
        paper_node1 = self.ns[f'paper#{text_id1}']
        paper_node2 = self.ns[f'paper#{text_id2}']
        self.graph.add((paper_node1, self.ns['similar_to'], similarity_node))
        self.graph.add((similarity_node, self.ns['similar_from'], paper_node2))