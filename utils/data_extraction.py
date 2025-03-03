import chromadb
from sentence_transformers import SentenceTransformer
from chunking import split_conversations, forgot_password_chunk

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

KEYWORDS = {"login", "username", "password", "account"}

def filter_relevant_chunks(chunks):
    relevant_chunks = [chunk for chunk in chunks if any(keyword in chunk.lower() for keyword in KEYWORDS)]
    return relevant_chunks

def store_in_vector_db(chunks):
    client = chromadb.PersistentClient(path="new_vector_db/")
    collection = client.get_or_create_collection(name="login_related_chunks")
    
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        collection.add(ids=[str(i+1168)], embeddings=[embedding], documents=[chunk])
    
    return collection

# def process_pdf():
#     chunks = split_conversations()
#     print(f"Extracted {len(chunks)} chunks from the PDF.")
#     relevant_chunks = filter_relevant_chunks(chunks)
#     print(f"Found {len(relevant_chunks)} relevant chunks.")
#     if relevant_chunks:
#         collection = store_in_vector_db(relevant_chunks)
#         print("Collection count:", collection.count())
#         print(f"Stored {len(relevant_chunks)} relevant chunks in ChromaDB.")
#     else:
#         print("No relevant chunks found.")

def process_pdf():
    chunks = forgot_password_chunk()
    print(f"Extracted {len(chunks)} chunks from the reset password pdfs")
    # relevant_chunks = filter_relevant_chunks(chunks)
    # print(f"Found {len(relevant_chunks)} relevant chunks.")
    if chunks:
        collection = store_in_vector_db(chunks)
        print("Collection count:", collection.count())
        print(f"Stored {len(chunks)} relevant chunks in ChromaDB.")
    else:
        print("No relevant chunks found.")

process_pdf()