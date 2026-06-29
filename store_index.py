
# from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from typing import List
# from langchain_core.documents import Document
# from langchain_google_genai import ChatGoogleGenerativeAI

# from langchain_core.prompts import ChatPromptTemplate

# from langchain_huggingface import HuggingFaceEmbeddings


# # Extract text from PDF files
# def load_pdf_files(data):
#     loader = DirectoryLoader(
#         data,
#         glob="*.pdf",
#         loader_cls=PyPDFLoader
#     )

#     documents = loader.load()
#     return documents
# extracted_data = load_pdf_files("data")



# def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
#     """
#     Given a list of Document objects, return a new list of Document objects
#     containing only 'source' in metadata and the original page_content.
#     """
#     minimal_docs: List[Document] = []
#     for doc in docs:
#         src = doc.metadata.get("source")
#         minimal_docs.append(
#             Document(
#                 page_content=doc.page_content,
#                 metadata={"source": src}
#             )
#         )
#     return minimal_docs
# minimal_docs = filter_to_minimal_docs(extracted_data)
# minimal_docs

# # Split the documents into smaller chunks
# def text_split(minimal_docs):
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=20,
#     )
#     texts_chunk = text_splitter.split_documents(minimal_docs)
#     return texts_chunk
# texts_chunk = text_split(minimal_docs)
# print(f"Number of chunks: {len(texts_chunk)}")
# texts_chunk
# # from langchain.embeddings import HuggingFaceEmbeddings

# # def download_embeddings():
# #     """
# #     Download and return the HuggingFace embeddings model.
# #     """
# #     model_name = "sentence-transformers/all-MiniLM-L6-v2"
# #     embeddings = HuggingFaceEmbeddings(
# #         model_name=model_name
# #     )
# #     return embeddings

# # embedding = download_embeddings()

# def download_embeddings():
#     model_name = "sentence-transformers/all-MiniLM-L6-v2"

#     embeddings = HuggingFaceEmbeddings(
#         model_name=model_name
#     )

#     return embeddings

# embedding = download_embeddings()
# embedding
# vector = embedding.embed_query("Hello world")
# vector
# print( "Vector length:", len(vector))
# from dotenv import load_dotenv
# import os
# load_dotenv()
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
# os.environ["EMINI_API_KEY"] = GEMINI_API_KEY
# from pinecone import Pinecone 
# pinecone_api_key = PINECONE_API_KEY

# pc = Pinecone(api_key=pinecone_api_key)
# pc

# from pinecone import ServerlessSpec 

# index_name = "medical-chatbot"

# if not pc.has_index(index_name):
#     pc.create_index(
#         name = index_name,
#         dimension=384,  # Dimension of the embeddings
#         metric= "cosine",  # Cosine similarity
#         spec=ServerlessSpec(cloud="aws", region="us-east-1")
#     )


# index = pc.Index(index_name)
# # Load Existing index 

# from langchain_pinecone import PineconeVectorStore
# # Embed each chunk and upsert the embeddings into your Pinecone index.
# docsearch = PineconeVectorStore.from_existing_index(
#     index_name=index_name,
#     embedding=embedding
# )
# dswith = Document(
#     page_content="Iam Rajasri.I need to study DSA for my placements.Iam thinking that i unable to complete  my goals.",
#     metadata={"source": "Youtube"}
# )
# docsearch.add_documents(documents=[dswith])
# retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})
# retrieved_docs = retriever.invoke("What is Acne?")
# retrieved_docs



# prompt = ChatPromptTemplate.from_template("""
# Use the context to answer the question.

# Context:
# {context}

# Question:
# {question}
# """)
# import os
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI

# load_dotenv()

# chatModel = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=os.getenv("GEMINI_API_KEY")
# )

# system_prompt = (
#     "You are a Medical assistant for question-answering tasks. "
#     "Use the following pieces of retrieved context to answer "
#     "the question. If you don't know the answer, say that you don't know. "
#     "Use three sentences maximum and keep the answer concise.\n\n"
#     "{context}"
# )

# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_prompt),
#         ("human", "{input}"),
#     ]
# )
# # question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
# # rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# from langchain_google_genai import ChatGoogleGenerativeAI
# print("Gemini OK")
# from langchain_google_genai import ChatGoogleGenerativeAI
# import os

# chatModel = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=os.getenv("GEMINI_API_KEY")
# )

# response = chatModel.invoke("What is diabetes?")
# print(response.content)
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import ChatPromptTemplate

# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=os.getenv("GEMINI_API_KEY")
# )

# prompt = ChatPromptTemplate.from_template("""
                                          
# you are my medical assistant.
# Answer the question using the provided context.

# Context:
# {context}

# Question:
# {question}
# """)

# chain = prompt | llm
# print("retriever" in globals())
# question = "What is Acne?"

# docs = retriever.invoke(question)

# context = "\n\n".join(doc.page_content for doc in docs)

# response = chain.invoke({
#     "context": context,
#     "question": question
# })

# print(response.content)
# print("docsearch" in globals())
# question = "what is Acromegaly and gigantism?"

# docs = retriever.invoke(question)

# context = "\n\n".join(doc.page_content for doc in docs)

# response = chain.invoke({
#     "context": context,
#     "question": question
# })

# print(response.content)


# import os
# from dotenv import load_dotenv
# # from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
# from langchain_community.document_loaders import PyPDFium2Loader, DirectoryLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.documents import Document
# from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
# from langchain_pinecone import PineconeVectorStore
# from pinecone import Pinecone, ServerlessSpec
# from langchain_huggingface import HuggingFaceEmbeddings  

# # ── 1. LOAD ENVIRONMENT VARIABLES ─────────────────────────────
# load_dotenv()

# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # Set them explicitly in the environment for LangChain wrappers
# os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
# os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# # ── 2. EXTRACT TEXT FROM PDF FILES ────────────────────────────
# # def load_pdf_files(data_directory):
# #     loader = DirectoryLoader(
# #         data_directory,
# #         glob="*.pdf",
# #         loader_cls=PyPDFLoader
# #     )
# #     documents = loader.load()
# #     return documents
# def load_pdf_files(data):
#     loader = DirectoryLoader(
#         data,
#         glob="*.pdf",
#         loader_cls=PyPDFium2Loader  # <-- Changed to PyPDFium2Loader
#     )

#     documents = loader.load()
#     return documents

# print("Loading PDF files from directory...")
# extracted_data = load_pdf_files("data")

# # Clean up document metadata to keep only the source track
# def filter_to_minimal_docs(docs):
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

# minimal_docs = filter_to_minimal_docs(extracted_data)

# # ── 3. SPLIT TEXT INTO CHUNKS ──────────────────────────────────
# def text_split(docs):
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=20,
#     )
#     return text_splitter.split_documents(docs)

# texts_chunk = text_split(minimal_docs)
# print(f"Total processed text chunks: {len(texts_chunk)}")

# # # ── 4. INITIALIZE GOOGLE EMBEDDINGS ───────────────────────────
# # def download_embeddings():
# #     """Download and return the Google GenAI embeddings model."""
# #     embeddings = GoogleGenerativeAIEmbeddings(  # <-- Changed
# #         model="text-embedding-004",  # Keep this as text-embedding-004
# #         google_api_key=GEMINI_API_KEY
# #     )
# #     return embeddings

# # embedding = download_embeddings()

# # # ── 5. PINECONE CLIENT SETUP & INDEX INGESTION ────────────────
# # index_name = "medical-chatbot"

# # # Initialize Pinecone Client
# # pc = Pinecone(api_key=PINECONE_API_KEY)

# # # Safety check: Create the index if it doesn't exist yet with 768 dimensions
# # if not pc.has_index(index_name):
# #     print(f"Index '{index_name}' not found. Creating a new 768-dimension index...")
# #     pc.create_index(
# #         name=index_name,
# #         dimension=768,  # Size needed for text-embedding-004
# #         metric="cosine",
# #         spec=ServerlessSpec(cloud="aws", region="us-east-1")
# #     )

# # print(f"Uploading vectors to your empty '{index_name}' index in Pinecone...")

# # # Embed chunks and push them directly to Pinecone
# # docsearch = PineconeVectorStore.from_documents(
# #     documents=texts_chunk,
# #     embedding=embedding,
# #     index_name=index_name
# # )

# # print("🎉 Successfully uploaded all medical vectors to Pinecone!")

# # ── 4. INITIALIZE GOOGLE EMBEDDINGS ───────────────────────────
# # ── 4. INITIALIZE GOOGLE EMBEDDINGS ───────────────────────────
# # ── 4. INITIALIZE GOOGLE EMBEDDINGS ───────────────────────────
# # ── 4. INITIALIZE LOCAL HUGGINGFACE EMBEDDINGS ────────────────
# from langchain_huggingface import HuggingFaceEmbeddings

# def download_embeddings():
#     """Download and return a local 768-dimension embedding model."""
#     print("Initializing local Hugging Face embedding model (768 dimensions)...")
#     embeddings = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-mpnet-base-v2"
#     )
#     return embeddings

# embedding = download_embeddings()

# # ── 5. PINECONE CLIENT SETUP & BATCH INGESTION ────────────────
# index_name = "medical-chatbot"

# # Initialize Pinecone Client
# pc = Pinecone(api_key=PINECONE_API_KEY)

# if not pc.has_index(index_name):
#     print(f"Index '{index_name}' not found. Creating a new 768-dimension index...")
#     pc.create_index(
#         name=index_name,
#         dimension=768,  
#         metric="cosine",
#         spec=ServerlessSpec(cloud="aws", region="us-east-1")
#     )

# print(f"Starting batch upload of {len(texts_chunk)} vectors to 'medical-chatbot'...")

# # Initialize the vector store empty linked to your index
# docsearch = PineconeVectorStore(index_name=index_name, embedding=embedding)

# # Process in safe chunks of 1,000 to prevent API rate limits and timeouts
# batch_size = 1000
# for i in range(0, len(texts_chunk), batch_size):
#     batch = texts_chunk[i:i + batch_size]
#     print(f"Uploading batch {i // batch_size + 1}/{(len(texts_chunk) // batch_size) + 1} ({len(batch)} chunks)...")
#     docsearch.add_documents(documents=batch)

# print("🎉 Successfully uploaded all 40,257 medical vectors to Pinecone!")
"""
store_index.py — Uses sentence-transformers locally for indexing.
NO API quota. NO rate limits. Runs completely offline.
Model: all-mpnet-base-v2 → 768 dimensions
Run once locally, then deploy app to Render.
"""
import os, time
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import pypdf

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME       = "medical-chatbot"
PDF_PATH         = "data/Medical book.pdf"
CHUNK_SIZE       = 500
CHUNK_OVERLAP    = 50
BATCH_SIZE       = 100   # large batch — no API limits!
PROGRESS_FILE    = "progress.txt"

# ── STEP 1: Load embedding model (downloads once, ~420MB) ─────
print("Loading embedding model (downloads once ~420MB)...")
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
print("Model loaded.")

# ── STEP 2: Read PDF ──────────────────────────────────────────
print(f"\nOpening: {PDF_PATH}")
reader      = pypdf.PdfReader(PDF_PATH)
total_pages = len(reader.pages)
print(f"Total pages: {total_pages}")

all_text = []
for i, page in enumerate(reader.pages):
    if i % 200 == 0:
        print(f"  Reading page {i+1}/{total_pages}...", flush=True)
    try:
        text = (page.extract_text() or "").strip()
        if text:
            all_text.append(text)
    except Exception:
        pass

print(f"Extracted text from {len(all_text)} pages")

# ── STEP 3: Chunk ─────────────────────────────────────────────
print("Chunking...")
chunks = []
for page_text in all_text:
    words = page_text.split()
    start = 0
    while start < len(words):
        chunk = " ".join(words[start : start + CHUNK_SIZE])
        if chunk.strip():
            chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP

print(f"Total chunks: {len(chunks)}")

# ── STEP 4: Pinecone — dimension=768 ─────────────────────────
print("\nConnecting to Pinecone...")
pc = Pinecone(api_key=PINECONE_API_KEY)

if pc.has_index(INDEX_NAME):
    print(f"Deleting old index (wrong dimensions from yesterday)...")
    pc.delete_index(INDEX_NAME)
    time.sleep(8)

print("Creating index with dimension=768...")
pc.create_index(
    name=INDEX_NAME,
    dimension=768,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)
time.sleep(10)
index = pc.Index(INDEX_NAME)
print("Pinecone ready.")

# ── STEP 5: Resume support ────────────────────────────────────
start_batch = 0
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE) as f:
        val = f.read().strip()
        if val.isdigit():
            start_batch = int(val)
            print(f"Resuming from batch {start_batch + 1}")

total_batches = (len(chunks) - 1) // BATCH_SIZE + 1
print(f"\nUploading {len(chunks)} chunks in {total_batches} batches of {BATCH_SIZE}...")
print("(No API quota — running at full speed)\n")

# ── STEP 6: Embed + Upload (local, no quota) ──────────────────
for i in range(start_batch * BATCH_SIZE, len(chunks), BATCH_SIZE):
    batch     = chunks[i : i + BATCH_SIZE]
    batch_num = i // BATCH_SIZE + 1
    print(f"  Batch {batch_num}/{total_batches} ({len(batch)} chunks)...", end=" ", flush=True)

    try:
        # Local embedding — instant, no internet needed
        vectors_values = model.encode(batch, show_progress_bar=False).tolist()

        vectors = [
            {
                "id":       f"chunk-{i + j}",
                "values":   vectors_values[j],
                "metadata": {"text": batch[j], "source": PDF_PATH}
            }
            for j in range(len(batch))
        ]
        index.upsert(vectors=vectors)
        print("done")

        # Save progress
        with open(PROGRESS_FILE, "w") as f:
            f.write(str(batch_num))

    except Exception as e:
        print(f"FAILED: {e}")

print(f"\nDone! {len(chunks)} vectors uploaded to '{INDEX_NAME}'.")
if os.path.exists(PROGRESS_FILE):
    os.remove(PROGRESS_FILE)
print("You can now deploy to Render!")