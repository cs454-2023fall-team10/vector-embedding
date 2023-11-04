import openai, numpy as np

with open("api_key", "r") as key :
    openai.api_key = key.read()

resp = openai.Embedding.create(
    input=["feline friends say", "meow"],
    engine="text-similarity-davinci-001")

embedding_a = resp['data'][0]['embedding']
embedding_b = resp['data'][1]['embedding']

similarity_score = np.dot(embedding_a, embedding_b)