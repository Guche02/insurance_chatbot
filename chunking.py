import pandas as pd
import PyPDF2
from pandas import DataFrame



def split_qna():
    
    """Creates chunks of conversation for csv data"""
    
    df = pd.read_csv("./data/Ticket Bot Issues and Answers from Office_Knowledge_Base.csv")
    
    #drop rows with null values
    df.dropna()
    #chunk list
    chunks = []
    for index, row in df.iterrows():    
        #format
        formatted_entry = f"Question: {row['Question/Issue']} Answer: {row['Answer/Solution']}" 
        #append
        chunks.append(formatted_entry)
    return chunks
            

def split_conversations():
    """The function takes in the converations pdf 
    including user question/issue, moderator reply, chatbot reply
    and splits each conversation into individual chunks."""
    text = ""
    with open("./data/processed_data.pdf", "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    lines = text.split("\n")
    chunks = []
    current_issue = ""
    
    for index, line in enumerate(lines, start=1):
        #in the data issues/question are prefixed with these two strings
        if "Issue:" in line or "User:" in line:
            if current_issue:
                chunks.append(current_issue) 
            current_issue = line 
        else:
            current_issue += " " + line 
    
    if current_issue:  
        chunks.append(current_issue)
    
    chunks = [i for i in chunks if i] 
    
    return chunks

   
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_experimental.text_splitter import SemanticChunker

#embedding for semantic splitter
hf_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#define semantic chunker
text_splitter = SemanticChunker(
    hf_embeddings, breakpoint_threshold_type="standard_deviation",
)
 
def split_bronze_plan():
    text = ""
    with open("./data/bronze_plan.pdf", "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
        chunks = text_splitter.split_text(text)
        return chunks


def forgot_password_chunk():
    chunks= []
    file_list = ["./data/reset_agent_username_password.pdf","./data/reset_group_username_password.pdf","./data/reset_member_username_password.pdf"]

    for file_name in file_list: 
        with open(file_name, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            chunks.append(text)
    return chunks 

#The code below gets value before : in each line and returns the unique onces
# lines = text.split("\n")
# unique_values = set()

# for line in lines:
#     line = line.strip()  # Remove extra spaces/newlines
#     if ":" in line:
#         unique_values.add(line.split(":")[0])  # Add unique values before ':'

# for value in unique_values:
#     print(value)
