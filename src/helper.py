# from typing import List
    

# from langchain_community.document_loaders import (
#     PyPDFLoader,
#     DirectoryLoader
# )

# from langchain_text_splitters import (
#     RecursiveCharacterTextSplitter
# )

# from langchain_huggingface import (
#     HuggingFaceEmbeddings
# )

# from langchain_core.documents import Document


# # Extract Data From PDF Files
# def load_pdf_file(data):
#     loader = DirectoryLoader(
#         data,
#         glob="*.pdf",
#         loader_cls=PyPDFLoader
#     )

#     documents = loader.load()
#     return documents


# def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
#     """
#     Given a list of Document objects, return a new list
#     containing only source metadata and page content.
#     """

#     minimal_docs = []

#     for doc in docs:
#         src = doc.metadata.get("source")

#         minimal_docs.append(
#             Document(
#                 page_content=doc.page_content,
#                 metadata={"source": src}
#             )
#         )

#     return minimal_docs


# # Split the Data into Text Chunks
# def text_split(extracted_data):
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=20
#     )

#     text_chunks = text_splitter.split_documents(
#         extracted_data
#     )

#     return text_chunks


# # Download Embeddings From HuggingFace
# def download_hugging_face_embeddings():

#     embeddings = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-MiniLM-L6-v2"
#     )

#     return embeddings

# from langchain_huggingface import HuggingFaceEmbeddings

# def download_hugging_face_embeddings():
#     return HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-MiniLM-L6-v2"
#     )
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

def download_hugging_face_embeddings():
    """Fixed model string name to prevent 404 API error."""
    return GoogleGenerativeAIEmbeddings(
        model="text-embedding-004",  # <-- Removed 'models/' prefix
        google_api_key=os.getenv("GEMINI_API_KEY")
    )