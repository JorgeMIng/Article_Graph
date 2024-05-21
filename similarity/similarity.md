# Model for Text Similarity Using Sentence Transformers
This README provides an overview of how to use the provided Python class Model to calculate the cosine similarity between pairs of texts using Sentence Transformers and scikit-learn's cosine_similarity.

## Prerequisites
Before using this class, ensure you have the necessary libraries installed. You can install them using pip:

```sh
pip install -U sentence-transformers
```

## Class Initialization
To initialize the class, you need to provide:

- A list of texts (texts): These are the texts for which you want to calculate similarity.
- A model name (model_name): This is the name of the pre-trained SentenceTransformer model you want to use for encoding the texts.

## Methods
'__init__(self, texts, model_name)'
This is the constructor method that initializes the class with the provided texts and model name.

### Arguments:

- texts (list): A list of texts to be used for similarity calculation.
- model_name (str): The name of the SentenceTransformer model to use.
'calculate_similarity(self)'
This method calculates the cosine similarity between all pairs of texts.

### Returns:
A list of dictionaries, where each dictionary contains:
- text_id1 (int): Index of the first text in the pair.
- text_id2 (int): Index of the second text in the pair.
- similarity (float): Cosine similarity score between the two texts.

# Usage example
In examples/examples_similarity.ipynb
