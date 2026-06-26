# from flask import Flask, render_template, request
# import os
# from dotenv import load_dotenv

# from langchain_pinecone import PineconeVectorStore
# from langchain_google_genai import ChatGoogleGenerativeAI

# from langchain.chains import create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate

# from src.helper import download_embeddings
# from src.prompt import system_prompt

# # ---------------- INIT ---------------- #
# app = Flask(__name__)
# load_dotenv()

# os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
# os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

# # ---------------- EMBEDDINGS ---------------- #
# embeddings = download_embeddings()

# # ---------------- VECTOR DB ---------------- #
# index_name = "medical-chatbot"

# docsearch = PineconeVectorStore.from_existing_index(
#     index_name=index_name,
#     embedding=embeddings
# )

# retriever = docsearch.as_retriever(
#     search_type="similarity",
#     search_kwargs={"k": 3}
# )

# # ---------------- LLM ---------------- #
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=os.getenv("GEMINI_API_KEY"),
#     temperature=0.3
# )

# # ---------------- PROMPT ---------------- #
# prompt = ChatPromptTemplate.from_messages([
#     ("system", system_prompt),
#     ("human", "{input}")
# ])

# # ---------------- RAG CHAIN ---------------- #
# doc_chain = create_stuff_documents_chain(llm, prompt)

# rag_chain = create_retrieval_chain(
#     retriever,
#     doc_chain
# )

# # ---------------- ROUTES ---------------- #
# @app.route("/")
# def home():
#     return render_template("chat.html")


# @app.route("/get", methods=["POST"])
# def get_response():
#     try:
#         user_msg = request.form.get("msg")

#         if not user_msg:
#             return "No input received"

#         result = rag_chain.invoke({"input": user_msg})

#         answer = result.get("answer")

#         if not answer:
#             return str(result)

#         return answer

#     except Exception as e:
#         return f"Error: {str(e)}"
   


# # ---------------- RUN ---------------- #
# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=8080)
import sys
print("=" * 60)
print(sys.executable)
print("=" * 60)

from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

from src.helper import download_hugging_face_embeddings
from src.prompt import system_prompt

from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


# ---------------------------
# Flask App
# ---------------------------
app = Flask(__name__)


# ---------------------------
# Load Environment Variables
# ---------------------------
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY


# ---------------------------
# Load Embedding Model
# ---------------------------
embeddings = download_hugging_face_embeddings()


# ---------------------------
# Connect to Existing Pinecone Index
# ---------------------------
index_name = "medical-chatbot"

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)


# ---------------------------
# Create Retriever
# ---------------------------
retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k":3}
)


# ---------------------------
# Gemini Model
# ---------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY
)


# ---------------------------
# Prompt Template
# ---------------------------
prompt = ChatPromptTemplate.from_template("""
{system_prompt}

Context:
{context}

Question:
{question}
""")


# ---------------------------
# Home Page
# ---------------------------
@app.route("/")
def index():
    return render_template("chat.html")


# ---------------------------
# Chat Route
# ---------------------------
# @app.route("/get", methods=["POST"])
# def chat():

#     question = request.form["msg"]

#     # Retrieve relevant documents
#     docs = retriever.invoke(question)

#     # Combine retrieved chunks
#     context = "\n\n".join(
#         doc.page_content for doc in docs
#     )

#     # Create final prompt
#     final_prompt = prompt.format(
#         system_prompt=system_prompt,
#         context=context,
#         question=question
#     )

#     # Gemini Response
#     response = llm.invoke(final_prompt)

#     return response.content

@app.route("/get", methods=["POST"])
def chat():
    try:
        question = request.form["msg"]

        docs = retriever.invoke(question)

        context = "\n\n".join(doc.page_content for doc in docs)

        final_prompt = prompt.format(
            system_prompt=system_prompt,
            context=context,
            question=question
        )

        response = llm.invoke(final_prompt)

        return response.content

    except Exception as e:
        import traceback
        traceback.print_exc()      # Prints the full error in the terminal
        return str(e), 500


# ---------------------------
# Run Flask
# ---------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )