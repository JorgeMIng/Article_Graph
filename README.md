# Article_Graph

[![Documentation Status](https://readthedocs.org/projects/article-graph-group-3/badge/?version=latest)](https://article-graph-group-3.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![DOI](https://zenodo.org/badge/785346462.svg)](https://zenodo.org/doi/10.5281/zenodo.11242795)

Article_Graph is a tool that extracts and enriches information from a
set of academic papers and journals.

It makes use of advanced and powerful machine learning tools to extract
as much information as possible.
Also, it uses [Grobid](https://grobid.readthedocs.io/en/latest/) to
extract all the relevant information about the papers.

The final output of this experiment is a RDF Graph that includes all the
extracted and reconciled information about the papers and their relations.

A simple application is also available to visualize and interact with
the KG.

## Requirements

**Python >= 3.11** is required for running the experiments.

**Grobid** is required for the first step of the pipeline, you can
follow the installation instructions
[here](https://grobid.readthedocs.io/en/latest/Run-Grobid/).

**PDF_ArticleAnalyzer** is required to interact with the **Grobid** service,
you can follow the installation instructions
[here](https://github.com/JorgeMIng/PDF_ArticleAnlyzer).

## Running the Application with Docker with the KG in a Remote Server

If you want to try the application with the pregenerated graph under
the `rdf` directory, here you will find all the instructions necessary for
running it.

1. Clone the repository:

```
git clone https://github.com/JorgeMIng/Article_Graph
cd Article_Graph
```

2. Build the Docker image:

```bash
docker build -t graph_tool docker
```

3. Run the image:

```bash
docker run -p 8501:8501 graph_tool
```

By default, the KG generated in the `examples/article_graph.ipynb` is
loaded in a remote server `http://yordi111nas.synology.me:3030/articles/query`.
The graph is also available under the `rdf` directory.

## Running the Application from Source with the KG in a Remote Server

If you want to try the application with the pregenerated graph under
the `rdf` directory, here you will find all the instructions necessary for
running it.

1. Clone the repository:

```
git clone https://github.com/JorgeMIng/Article_Graph
cd Article_Graph
```

2. Create a Python environment (conda is recommended):

```bash
conda create -n article-graph-3.11 python=3.11
conda activate article-graph-3.11
```

3. Install all the dependencies:

```bash
pip install -r requirements_app.txt
```

4. Execute the application:

```bash
python Start.py
```

By default, the KG generated in the `examples/article_graph.ipynb` is
loaded in a remote server `http://yordi111nas.synology.me:3030/articles/query`

## Running the Application with a custom KG Hosted Locally

If you want to try the application with another graph generated locally,
here you will find all the instructions necessary for running it.

1. Clone the repository:

```
git clone https://github.com/JorgeMIng/Article_Graph
cd Article_Graph
```

2. Create a Python environment (conda is recommended):

```bash
conda create -n article-graph-3.11 python=3.11
conda activate article-graph-3.11
```

3. Install all the dependencies:

```bash
pip install -r requirements_app.txt
```

4. Host the KG in Jena Fuseki with Docker:

```bash
docker run -p 3030:3030 stain/jena-fuseki
```

5. Execute the application:

```bash
python Start.py
```

6. Go to the _Settings_ section and configure the remote server.

## Running the Experiments

If you want to reproduce the experiments by yourself, here you will find
all the instructions necessary for running them.

1. Clone the repository:

```
git clone https://github.com/JorgeMIng/Article_Graph
cd Article_Graph
```

2. Create a Python environment (conda is recommended):

```bash
conda create -n article-graph-3.11 python=3.11
conda activate article-graph-3.11
```

3. Install all the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the example notebook at `examples/article_graph.ipynb`

## Examples

- Full KG Generation: `examples/article_graph.ipynb`
- Similarity Analysis: `examples/examples_similarity.ipynb`
- Topic Modeling: `examples/topic_modeling.ipynb`
- NER Analysis and Project extracton: `ner/extract_element.ipynb`

## License

Please refer to the `LICENSE` file.

## Authors

- Jorge Martín Izquierdo
- Gloria Cumia Espinosa de los Monteros
- Marco Ciccalè Baztán
