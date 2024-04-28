# all-MiniLM-L6-v2
# pip install -U sentence-transformers

# Lista de textos
texts = ["Her name is Ramona, she is very clever", "Ramona is a very intelligent woman", "It is very clever to name her Ramona"]

# Inicializar el modelo SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Calcular los embeddings para los textos
embeddings = model.encode(texts)

# Calcular la similitud coseno entre todos los pares de textos
similarity_scores = cosine_similarity(embeddings)

# Crear una lista para almacenar los resultados de similitud
resultados_similitud = []

# Llenar la lista con los resultados de similitud
for i in range(len(texts)):
    for j in range(i+1, len(texts)):
        # cada elemento de la lista es un diccionario
        resultado = {'idtexto1': i, 'idtexto2': j, 'similarity': similarity_scores[i][j]}
        resultados_similitud.append(resultado)

# Imprimir resultados
print("Resultados de similitud:")
for resultado in resultados_similitud:
    print(resultado)
