import PyPDF2
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker

#semantic text splitter used for splitting bronze plan text into chunks
hf_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_splitter = SemanticChunker(
    hf_embeddings, breakpoint_threshold_type="standard_deviation",
)

def get_enrollment_conversations():
    
    """The function takes in the converations pdf
    including user question/issue, moderator reply, chatbot reply
    and splits each conversation into individual chunks
    then filters out conversations related to enrollment and returns them"""
    
    text = ""
    with open("D:\insurance-chatbot\data\processed_data.pdf", "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    lines = text.split("\n")
    chunks = []
    current_issue = ""

    for index, line in enumerate(lines, start=1):
        if "Issue:" in line or "User:" in line:
            if current_issue:
                chunks.append(current_issue)
            current_issue = line
        else:
            current_issue += " " + line

    if current_issue:
        chunks.append(current_issue)

    chunks = [i for i in chunks if i]

    keyword_list = ['plan','enrollment','enroll','benifits']
    enrollement_conversation = []
    for i in chunks:
      for j in keyword_list:
        if j in i.lower():
          enrollement_conversation.append(i)

    return enrollement_conversation

    
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




