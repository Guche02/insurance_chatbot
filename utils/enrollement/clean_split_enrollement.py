import PyPDF2
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
import re

#semantic text splitter used for splitting bronze plan text into chunks
hf_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_splitter = SemanticChunker(
    hf_embeddings, breakpoint_threshold_type="standard_deviation",
)


def get_enrollment_conversations(pdf_path="D:/insurance-chatbot/data/processed_data.pdf"):
    """ 
    This function extracts conversations from a PDF, splits them into chunks,
    and filters out conversations related to enrollment.
    """
    text = []
    
    # Read the PDF and extract text
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text.append(page.extract_text())
    
    # Combine text from all pages
    full_text = " ".join(text)
    
    # Split the text into lines for processing
    lines = full_text.split("\n")
    
    # Initialize variables for chunking conversations
    chunks = []
    current_issue = ""
    
    # Iterate through each line and extract conversation chunks
    for line in lines:
        if "Issue:" in line or "User:" in line:
            if current_issue:
                chunks.append(current_issue.strip())
            current_issue = line
        else:
            current_issue += " " + line.strip()
    
    # Append the last chunk if exists
    if current_issue:
        chunks.append(current_issue.strip())
    
    # Filter out conversations related to enrollment using regex for keyword matching
    keyword_pattern = r'\b(plan|enrollment|enroll|benefits|tier|coverage|plans)\b'
    enrollment_conversations = [chunk for chunk in chunks if re.search(keyword_pattern, chunk, re.IGNORECASE)]

    return enrollment_conversations



    
def get_split_bronze_plan():
  processed_chunks = []  

  with open("D:\\insurance-chatbot\\data\\bronze_plan.pdf", "rb") as file:
      reader = PyPDF2.PdfReader(file)

      for i,page in enumerate(reader.pages):
          text = page.extract_text()

          if text:  
              lines = text.split("\n")
              first_two = " ".join(lines[:2])
              remaining_text = "\n".join(lines[2:])

              chunks = text_splitter.split_text(remaining_text)
              modified_chunks = [f"{first_two}\n{chunk}" for chunk in chunks]  
              
              processed_chunks.extend(modified_chunks) 
  return processed_chunks




