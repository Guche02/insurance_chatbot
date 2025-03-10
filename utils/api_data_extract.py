import chromadb   # type: ignore
import requests
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings   # type: ignore

API_URL_TEMPLATE = "https://api-tickets.corenroll.com/api/v2/coreyai-knowledge-base?page={}"

qa_pairs = []

for page in range(1, 9):
    url = API_URL_TEMPLATE.format(page)
    
    try:
        response = requests.get(url, timeout=10)  
        response.raise_for_status()  
        
        data = response.json()  
    
        if not isinstance(data, dict) or "data" not in data or "data" not in data["data"]:
            print(f" Unexpected response structure on page {page}")
            continue

        items = data["data"]["data"]

        for item in items:  
            if not isinstance(item, dict):
                print(f"Skipping invalid item on page {page}: {item}")
                continue

            query = item.get("query", "").strip()
            answer = item.get("answer", "").strip()

            if query and answer:
                qa_pairs.append({"query": query, "answer": answer})
                
    except requests.exceptions.RequestException as e:
        print(f"Request failed on page {page}: {e}")
    except ValueError as e:
        print(f"JSON decoding error on page {page}: {e}")

for i, qa in enumerate(qa_pairs[:10]):  
    print(f"🔹 {i+1}. Q: {qa['query']}\n   A: {qa['answer']}\n")

print(f"Extraction complete! {len(qa_pairs)} Q&A pairs collected.")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

PERSIST_DIRECTORY = "insurance_new"  
chroma_client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)

collection = chroma_client.get_or_create_collection(name="knowledge_base")

queries = [qa["query"] for qa in qa_pairs]
encoded_queries = model.encode(queries).tolist() 

for i, qa in enumerate(qa_pairs):
    doc_id = f"doc_{i}"  
    collection.add(
        ids=[doc_id],
        embeddings=[encoded_queries[i]],  
        documents=[f"Query: {qa['query']}\nAnswer: {qa['answer']}"]
    )
    print(f" Added: {qa['query'][:30]}...")

print(f"Data extraction, encoding, and storage completed! {len(qa_pairs)} Q&A pairs stored in ChromaDB.")