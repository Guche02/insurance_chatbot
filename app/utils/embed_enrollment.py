from clean_split_enrollement import get_enrollment_conversations, get_split_bronze_plan
from langchain.schema import Document
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
import uuid

enrollement_conversation = get_enrollment_conversations()
# bronze_plan = get_split_bronze_plan()
enrollement_chunks = enrollement_conversation
# enrollement_chunks = bronze_plan

print(f"Total number of chunks: {len(enrollement_chunks)}")

unique_enrollement_chunks = list(set(enrollement_chunks))

print(f"Total number of unique chunks: {len(unique_enrollement_chunks)}")


docs = [Document(page_content=chunk) for chunk in enrollement_chunks]

embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

client = PersistentClient(path="insurance_new")
# client = PersistentClient(path="insurance_vectordb/")

# client.delete_collection("enrollement_knowlage_base")

# collection = client.create_collection(name="enrollement_knowlage_base")
collection = client.get_collection(name="knowledge_base")

embeddings = embedding_model.encode(enrollement_chunks).tolist()

ids = [str(uuid.uuid4()) for _ in range(len(docs))]

collection.add(
    embeddings= embeddings,
    documents=enrollement_chunks,
    ids=ids,
    metadatas=[{"id":doc_id} for doc_id in ids] )

print(collection.count())