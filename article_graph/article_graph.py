"""
This module contains the class responsible for building an RDF graph.
"""

from rdflib import Graph, Namespace, Literal, OWL, URIRef
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

    def add_entity_data(self, entity_type_name, entity_id, relation, relation_data):
        """
        Auxiliar function to add data to an entity.
        """
        entity_uri = self.ns[f"{entity_type_name}#{entity_id}"]

        self.graph.add((entity_uri, self.ns[relation], relation_data))

    def add_wikidata_owl(self, entity_type_name, entity_id, wikidata_id):
        """
        Auxiliar function to add the sameAs property to an entity.
        """
        entity_uri = self.ns[f"{entity_type_name}#{entity_id}"]
        wikidata_uri = URIRef(f"https://www.wikidata.org/entity/{wikidata_id}")
        self.graph.add((entity_uri, OWL.sameAs, wikidata_uri))

    def add_paper(self, paper_id: int, title: str, abstract: str, release_date):
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
        if release_date is not None and not isinstance(release_date, str):
            release_date = release_date.text
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
        topic_belonging_fragment = f'topic_belonging#{paper_id}-{topic_id}'
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
        self.graph.add((similarity_node, RDFS.label, Literal(
            f'similarity-{text_id1}-{text_id2}')))
        self.graph.add((similarity_node, self.ns['degree'], Literal(
            similarity_score, datatype=XSD.float)))

        # Connect similarity to paper
        paper_node1 = self.ns[f'paper#{text_id1}']
        paper_node2 = self.ns[f'paper#{text_id2}']
        self.graph.add((paper_node1, self.ns['similar_to'], similarity_node))
        self.graph.add((similarity_node, self.ns['similar_from'], paper_node2))

    def add_organization(self, org_id, org_name, icon=None, coordinates=None, wikidata_id=None):
        org_uri = self.ns[f"organization#{org_id}"]
        self.graph.add((org_uri, RDF.type, self.ns.Organization))
        self.graph.add((org_uri, RDFS.label, Literal(org_name)))
        self.graph.add((org_uri, self.ns.name, Literal(org_name)))

        if icon:
            self.graph.add((org_uri, self.ns.icon, Literal(
                icon, datatype=XSD.anyURI)))

        if coordinates:
            self.graph.add((org_uri, self.ns.longitude, Literal(
                coordinates['lon'], datatype=XSD.float)))
            self.graph.add((org_uri, self.ns.latitude, Literal(
                coordinates['lat'], datatype=XSD.float)))

        if wikidata_id:
            self.add_wikidata_owl(
                'organization', entity_id=org_id, wikidata_id=wikidata_id)

    def add_organization_paper_relation(self, paper_id, organization_id):
        organization_uri = self.ns[f"organization#{organization_id}"]

        # URI del paper
        paper_uri = self.ns[f"paper#{paper_id}"]
        self.graph.add((paper_uri, self.ns.acknowledges, organization_uri))

    def add_organization_author_relation(self, author_id, organization_id):
        organization_uri = self.ns[f"organization#{organization_id}"]

        author_uri = self.ns[f"person#{author_id}"]

        # Agregar tripleta al grafo RDF
        self.graph.add((author_uri, self.ns.member, organization_uri))

    def add_project(self, project_id, project_name, project_federal_id):

        project_uri = self.ns[f"project#{project_id}"]

        # Crear la etiqueta del proyecto
        label = f"Award {project_name} {project_federal_id}"
        self.graph.add((project_uri, RDF.type, self.ns.Project))
        self.graph.add((project_uri, self.ns.name, Literal(
            project_name, datatype=XSD.string)))
        self.graph.add(
            (project_uri, RDFS.label, Literal(label, datatype=XSD.string)))
        self.graph.add((project_uri, self.ns.project_federal_id,
                       Literal(project_federal_id, datatype=XSD.string)))

    def add_project_relation(self, paper_id, project_id):
        project_uri = self.ns[f"project#{project_id}"]

        # URI del paper
        paper_uri = self.ns[f"paper#{paper_id}"]
        self.graph.add((paper_uri, self.ns.acknowledges, project_uri))

    def add_author(self,
                   author_id,
                   label,
                   first_name=None,
                   last_name=None,
                   email=None,
                   wikidata_id=None):
        author_uri = self.ns[f"person#{author_id}"]
        self.graph.add((author_uri, RDF.type, self.ns.Person))
        self.graph.add((author_uri, self.ns.label,
                       Literal(label, datatype=XSD.string)))

        if first_name:
            self.graph.add((author_uri, self.ns.first_name,
                           Literal(first_name, datatype=XSD.string)))
        if last_name:
            self.graph.add((author_uri, self.ns.last_name,
                           Literal(last_name, datatype=XSD.string)))
        if email:
            email_uri = URIRef(email)
            self.graph.add((author_uri, self.ns.email, email_uri))

        if wikidata_id:
            self.add_wikidata_owl(
                'person', entity_id=author_id, wikidata_id=wikidata_id)
