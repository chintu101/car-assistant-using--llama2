import ollama


with open("cat-facts.txt","r", encoding='utf-8') as file:
    dataset = file.readlines()
    print(f'loaded {len(dataset)} entries')

EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

VECTOR_DB = []

def add_chunk_to_database(chunk):
  embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0] #embedding existing data
  embedding = [float(x) for x in embedding]
  VECTOR_DB.append((chunk, embedding))

for i, chunk in enumerate(dataset):
    add_chunk_to_database(chunk)
    print(f'added chunk {i+1}/{len(dataset)} in vector database')


def cosine_similarity(a, b):
    print(a[0])
    dot_product = sum([x * y for x, y in zip(a, b)])
    norm_a = sum([x ** 2 for x in a]) ** 0.5
    norm_b = sum([x ** 2 for x in b]) ** 0.5
    return dot_product / (norm_a * norm_b)


def retrieve(query, top_n=3): #the top_n = 3 is to send the top 3 similar vectors
    query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=query)['embeddings'][0] #embedding the query
    similarities = []
    for c, embedding in VECTOR_DB:
        similarity = cosine_similarity(query_embedding, embedding) # calls cosine function to determine similarity
        similarities.append((c, similarity)) # c stands for the chunk, appends the chunk with its similarity to the input query

    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_n] #returns the top n similarities, right now n is set to 3


input_query = input("enter your question: ")
retrieved_knowledge = retrieve(input_query)
print('Retrieved knowledge:')

for chunk, similarity in retrieved_knowledge:
  print(f' - (similarity: {similarity:.2f}) {chunk}') #returns the similarities between the input and chunk vector upto two decimal places

instruction_prompt = f''' you are a helpful chatbot
Use only the following pieces of context to answer the question. Dont make up any new information:
{'/n'.join([f'{chunk}' for chunk, similarity in retrieved_knowledge])} 
'''

#using ollama to generate the prompt
stream = ollama.chat(
    model = LANGUAGE_MODEL,
    messages=[
        {'role': 'system', 'content': instruction_prompt},
        {'role': 'user', 'content': input_query}
    ],
    stream=True
)

print('chatbot responses: ')
for chunk in stream:
    print(chunk['message']['content'], end='', flush=True) #allowing us to see the chatbot response in real time










