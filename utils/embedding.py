from langchain.schema import Document
from chromadb import PersistentClient
from chromadb.config import Settings
from langchain.embeddings import SentenceTransformerEmbeddings 
from utils.chunking import split_qna, split_conversations, split_bronze_plan, forgot_password_chunk
from sentence_transformers import SentenceTransformer
import uuid
chunks = []
print(len(chunks))

qna = split_qna()
chunks= chunks+qna
print(len(chunks))

conversation = split_conversations()
chunks= chunks+conversation
print(len(chunks))

bronze_plan = split_bronze_plan()
chunks= chunks+bronze_plan
print(len(chunks))

forgot_password = forgot_password_chunk()
chunks= chunks+forgot_password
print(len(chunks))

# print(chunks[0])


docs = [Document(page_content=chunk) for chunk in chunks]

embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

client = PersistentClient(path="insurance/")

collection = client.get_or_create_collection(name="knowlage_base")

# collection = client.get_collection(name="knowlage_base")

#embed
embeddings = embedding_model.encode(chunks).tolist()

# print("chunks:")
# print(type(chunks))
# print(len(chunks))
# print(chunks[:2])

# print("embeddings:")
# print(type(embeddings))  # Should be numpy.ndarray or list
# print(len(embeddings))   # Should match len(chunks)
# print(embeddings[:2])    # Print first two embeddings


ids = [str(uuid.uuid4()) for _ in range(len(docs))]


# batch_size = 50  

# for i in range(0, len(chunks), batch_size):
#     batch_chunks = chunks[i:i+batch_size]
#     batch_ids = ids[i:i+batch_size]
#     batch_embeddings = embeddings[i:i+batch_size]
    
#     collection.add(
#         ids=batch_ids,  
#         documents=batch_chunks,  
#         embeddings=batch_embeddings
#     )
    
#     print(f"Added batch {i//batch_size + 1} with {len(batch_chunks)} documents")



# for index in range(len(chunks)):
#     print("enter loop")
#     try:
#         print("trying add")
#         collection.add(
#             embeddings=[embeddings[index]],  # Wrap in list
#             documents=[chunks[index]],       # Wrap in list
#             ids=[ids[index]],                # Wrap in list
#             metadatas=[{"id": ids[index]}]   # Metadata remains as a list
#         )
#         print(f"Added {ids[index]} successfully!")  # Debugging
#     except Exception as e:
#         print(f"Error adding {ids[index]}: {e}")  # Catch errors

# try:
#     collection.add(
#         embeddings=embeddings[:3].tolist(),  # Convert NumPy array to list
#         documents=chunks[:3],  # Already a list
#         ids=ids[:3],  # Already a list
#         metadatas=[{"id": doc_id} for doc_id in ids[:3]]  # List of metadata
#     )
#     print("All data added successfully!")
# except Exception as e:
#     print(f"Error adding data: {e}")

collection.add(
    embeddings= embeddings,
    documents=chunks,
    ids=ids,
    metadatas=[{"id":doc_id} for doc_id in ids] )


print(collection.count())