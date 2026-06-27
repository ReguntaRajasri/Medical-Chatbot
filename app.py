# # # from flask import Flask, render_template, request, session
# # # import sys
# # # print("=" * 60)
# # # print(sys.executable)
# # # print("=" * 60)

# # # from flask import Flask, render_template, request
# # # from dotenv import load_dotenv
# # # import os

# # # from src.helper import download_hugging_face_embeddings
# # # from src.prompt import system_prompt

# # # from langchain_pinecone import PineconeVectorStore
# # # from langchain_google_genai import ChatGoogleGenerativeAI
# # # from langchain_core.prompts import ChatPromptTemplate


# # # # ---------------------------
# # # # Flask App
# # # # ---------------------------
# # # app = Flask(__name__)


# # # # ---------------------------
# # # # Load Environment Variables
# # # # ---------------------------
# # # load_dotenv()

# # # PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# # # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # # os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
# # # os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY


# # # # ---------------------------
# # # # Load Embedding Model
# # # # ---------------------------
# # # embeddings = download_hugging_face_embeddings()


# # # # ---------------------------
# # # # Connect to Existing Pinecone Index
# # # # ---------------------------
# # # index_name = "medical-chatbot"

# # # docsearch = PineconeVectorStore.from_existing_index(
# # #     index_name=index_name,
# # #     embedding=embeddings
# # # )


# # # # ---------------------------
# # # # Create Retriever
# # # # ---------------------------
# # # retriever = docsearch.as_retriever(
# # #     search_type="similarity",
# # #     search_kwargs={"k":3}
# # # )


# # # # ---------------------------
# # # # Gemini Model
# # # # ---------------------------
# # # llm = ChatGoogleGenerativeAI(
# # #     model="gemini-2.5-flash",
# # #     google_api_key=GEMINI_API_KEY
# # # )


# # # # ---------------------------
# # # # Prompt Template
# # # # ---------------------------
# # # prompt = ChatPromptTemplate.from_template("""
# # # {system_prompt}

# # # Context:
# # # {context}

# # # Question:
# # # {question}
# # # """)


# # # # ---------------------------
# # # # Home Page
# # # # ---------------------------
# # # @app.route("/")
# # # def index():
# # #     return render_template("chat.html")



# # # @app.route("/get", methods=["POST"])
# # # def chat():
# # #     try:
# # #         question = request.form["msg"]

# # #         docs = retriever.invoke(question)

# # #         context = "\n\n".join(doc.page_content for doc in docs)

# # #         final_prompt = prompt.format(
# # #             system_prompt=system_prompt,
# # #             context=context,
# # #             question=question
# # #         )

# # #         response = llm.invoke(final_prompt)

# # #         return response.content

# # #     except Exception as e:
# # #         import traceback
# # #         traceback.print_exc()      # Prints the full error in the terminal
# # #         return str(e), 500


# # # # ---------------------------
# # # # Run Flask
# # # # ---------------------------
# # # if __name__ == "__main__":
# # #     app.run(
# # #         host="0.0.0.0",
# # #         port=8080,
# # #         debug=True
# # #     )




# # from flask import Flask, render_template, request, session
# # import sys
# # import os
# # import traceback
# # from dotenv import load_dotenv

# # print("=" * 60)
# # print(sys.executable)
# # print("=" * 60)

# # from src.helper import download_hugging_face_embeddings
# # from src.prompt import system_prompt

# # from langchain_pinecone import PineconeVectorStore
# # from langchain_google_genai import ChatGoogleGenerativeAI
# # from langchain_core.prompts import ChatPromptTemplate

# # # ----------------------------------------------------
# # # Flask App
# # # ----------------------------------------------------
# # app = Flask(__name__)
# # app.secret_key = "medical_chatbot_secret_key"

# # # ----------------------------------------------------
# # # Load Environment Variables
# # # ----------------------------------------------------
# # load_dotenv()

# # PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
# # os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# # # ----------------------------------------------------
# # # Embedding Model
# # # ----------------------------------------------------
# # embeddings = download_hugging_face_embeddings()

# # # ----------------------------------------------------
# # # Pinecone Vector Store
# # # ----------------------------------------------------
# # index_name = "medical-chatbot"

# # docsearch = PineconeVectorStore.from_existing_index(
# #     index_name=index_name,
# #     embedding=embeddings
# # )

# # retriever = docsearch.as_retriever(
# #     search_type="similarity",
# #     search_kwargs={"k":3}
# # )

# # # ----------------------------------------------------
# # # Gemini Model
# # # ----------------------------------------------------
# # llm = ChatGoogleGenerativeAI(
# #     model="gemini-2.5-flash",
# #     google_api_key=GEMINI_API_KEY,
# #     temperature=0.3
# # )

# # # ----------------------------------------------------
# # # Prompt
# # # ----------------------------------------------------
# # prompt = ChatPromptTemplate.from_template("""
# # {system_prompt}

# # You are a helpful medical AI assistant.

# # Use BOTH the previous conversation and the retrieved medical context
# # to answer the user's current question.

# # Previous Conversation:
# # {history}

# # Medical Context:
# # {context}

# # Current Question:
# # {question}

# # If the answer is not available in the medical context,
# # say you don't know.

# # Answer:
# # """)

# # # ----------------------------------------------------
# # # Home Page
# # # ----------------------------------------------------
# # @app.route("/")
# # def index():

# #     if "history" not in session:
# #         session["history"] = []

# #     return render_template("chat.html")

# # # ----------------------------------------------------
# # # Chat Route
# # # ----------------------------------------------------
# # @app.route("/get", methods=["POST"])
# # def chat():

# #     try:

# #         question = request.form["msg"]

# #         # -----------------------------
# #         # Conversation Memory
# #         # -----------------------------
# #         if "history" not in session:
# #             session["history"] = []

# #         history = session["history"]

# #         history_text = ""

# #         for chat in history:
# #             history_text += f"User: {chat['user']}\n"
# #             history_text += f"Assistant: {chat['assistant']}\n\n"

# #         # -----------------------------
# #         # Retrieve Documents
# #         # -----------------------------
# #         docs = retriever.invoke(question)

# #         context = "\n\n".join(
# #             doc.page_content
# #             for doc in docs
# #         )

# #         # -----------------------------
# #         # Final Prompt
# #         # -----------------------------
# #         final_prompt = prompt.format(
# #             system_prompt=system_prompt,
# #             history=history_text,
# #             context=context,
# #             question=question
# #         )

# #         # -----------------------------
# #         # Gemini Response
# #         # -----------------------------
# #         response = llm.invoke(final_prompt)

# #         answer = response.content

# #         # -----------------------------
# #         # Save Conversation
# #         # -----------------------------
# #         history.append({
# #             "user": question,
# #             "assistant": answer
# #         })

# #         # Keep only last 5 conversations
# #         history = history[-5:]

# #         session["history"] = history

# #         return answer

# #     except Exception as e:
# #         traceback.print_exc()
# #         return str(e),500

# # # ----------------------------------------------------
# # # Clear Memory
# # # ----------------------------------------------------
# # @app.route("/clear")
# # def clear():

# #     session.clear()

# #     return "Conversation Cleared"

# # # ----------------------------------------------------
# # # Run
# # # ----------------------------------------------------
# # if __name__=="__main__":

# #     app.run(
# #         host="0.0.0.0",
# #         port=8080,
# #         debug=True
# #     )

# from flask import Flask, render_template, request, session
# from dotenv import load_dotenv
# import os
# import traceback

# from src.helper import download_hugging_face_embeddings
# from src.prompt import system_prompt
# from langchain_pinecone import PineconeVectorStore
# from langchain_google_genai import ChatGoogleGenerativeAI

# # ── ENV ───────────────────────────────────────────────────────
# load_dotenv()

# PINECONE_API_KEY = os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
# GEMINI_API_KEY   = os.environ["GEMINI_API_KEY"]   = os.getenv("GEMINI_API_KEY")

# # ── FLASK ─────────────────────────────────────────────────────
# app = Flask(__name__)
# app.secret_key = os.getenv("FLASK_SECRET_KEY", "medical_chatbot_secret")

# # ── RAG SETUP ─────────────────────────────────────────────────
# embeddings = download_hugging_face_embeddings()

# retriever = PineconeVectorStore.from_existing_index(
#     index_name="medical-chatbot",
#     embedding=embeddings
# ).as_retriever(search_type="similarity", search_kwargs={"k": 3})

# # ── LLM ───────────────────────────────────────────────────────
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=GEMINI_API_KEY,
#     temperature=0.3
# )

# # ── CONSTANTS ─────────────────────────────────────────────────
# MAX_HISTORY = 5  # last N exchanges to keep in memory

# # ── MEMORY HELPERS ────────────────────────────────────────────
# def get_history() -> list:
#     return session.get("history", [])

# def format_history_for_prompt(history: list) -> str:
#     """Convert history list into readable text for the LLM."""
#     if not history:
#         return "No previous conversation."
#     return "".join(
#         f"User: {h['user']}\nAssistant: {h['assistant']}\n\n"
#         for h in history
#     )

# def save_to_history(user_msg: str, bot_reply: str) -> None:
#     history = session.setdefault("history", [])
#     history.append({"user": user_msg, "assistant": bot_reply})
#     session["history"] = history[-MAX_HISTORY:]
#     session.modified = True

# def build_context_aware_query(question: str, history: list) -> str:
#     """
#     If the question is vague/short (e.g. 'what are the treatments?'),
#     enrich it with the last topic from history so retrieval works correctly.
#     """
#     if len(question.split()) <= 6 and history:
#         last_topic = history[-1]["user"]
#         return f"{last_topic} {question}"
#     return question

# # ── ROUTES ────────────────────────────────────────────────────
# @app.route("/")
# def home():
#     session.setdefault("history", [])
#     return render_template("chat.html")


# @app.route("/get", methods=["POST"])
# def chat():
#     try:
#         question = request.form["msg"].strip()
#         if not question:
#             return "Please ask a question."

#         history = get_history()

#         # Use enriched query for retrieval so follow-ups get right docs
#         retrieval_query = build_context_aware_query(question, history)
#         docs = retriever.invoke(retrieval_query)
#         context = "\n\n".join(doc.page_content for doc in docs)

#         history_text = format_history_for_prompt(history)

#         # Build the full prompt as a plain string — gives full control
#         full_prompt = f"""{system_prompt}

# ---

# CONVERSATION HISTORY (use this for follow-up questions):
# {history_text}

# ---

# RELEVANT MEDICAL CONTEXT (from knowledge base):
# {context}

# ---

# CURRENT USER QUESTION:
# {question}

# ---

# INSTRUCTIONS:
# - If the question is a follow-up (e.g. "what are the treatments?"), 
#   refer back to the previous topic in conversation history.
# - Use the medical context to answer accurately.
# - If the answer is truly not available, say "I don't have enough information on that."
# - Be concise and clear.

# ANSWER:"""

#         answer = llm.invoke(full_prompt).content.strip()

#         save_to_history(question, answer)

#         return answer

#     except Exception:
#         traceback.print_exc()
#         return "Something went wrong. Please try again."


# @app.route("/clear")
# def clear():
#     session.pop("history", None)
#     return "Conversation cleared."


# # ── ENTRY POINT ───────────────────────────────────────────────
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080, debug=True)


# from flask import Flask, render_template, request, session
# from dotenv import load_dotenv
# import os
# import traceback
# import uuid

# from src.helper import download_hugging_face_embeddings
# from src.prompt import system_prompt
# from langchain_pinecone import PineconeVectorStore
# from langchain_google_genai import ChatGoogleGenerativeAI
# from db import init_db, save_message, get_history, clear_history

# # ── ENV ───────────────────────────────────────────────────────
# load_dotenv()

# PINECONE_API_KEY = os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
# GEMINI_API_KEY   = os.environ["GEMINI_API_KEY"]   = os.getenv("GEMINI_API_KEY")

# # ── FLASK ─────────────────────────────────────────────────────
# app = Flask(__name__)
# app.secret_key = os.getenv("FLASK_SECRET_KEY", "medical_chatbot_secret")

# # ── DB INIT ───────────────────────────────────────────────────
# init_db()

# # ── RAG SETUP ─────────────────────────────────────────────────
# embeddings = download_hugging_face_embeddings()

# retriever = PineconeVectorStore.from_existing_index(
#     index_name="medical-chatbot",
#     embedding=embeddings
# ).as_retriever(search_type="similarity", search_kwargs={"k": 3})

# # ── LLM ───────────────────────────────────────────────────────
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash-lite",
#     google_api_key=GEMINI_API_KEY,
#     temperature=0.3
# )

# # ── CONSTANTS ─────────────────────────────────────────────────
# MAX_HISTORY = 5

# # ── HELPERS ───────────────────────────────────────────────────
# def get_or_create_session_id() -> str:
#     """Each browser tab gets a unique session ID stored in Flask session."""
#     if "session_id" not in session:
#         session["session_id"] = str(uuid.uuid4())
#     return session["session_id"]

# def format_history_for_prompt(history: list) -> str:
#     if not history:
#         return "No previous conversation."
#     return "".join(
#         f"User: {h['user']}\nAssistant: {h['assistant']}\n\n"
#         for h in history
#     )

# def build_context_aware_query(question: str, history: list) -> str:
#     """Enrich short follow-up questions with previous topic for better retrieval."""
#     if len(question.split()) <= 6 and history:
#         last_topic = history[-1]["user"]
#         return f"{last_topic} {question}"
#     return question

# # ── ROUTES ────────────────────────────────────────────────────
# @app.route("/")
# def home():
#     get_or_create_session_id()
#     return render_template("chat.html")


# @app.route("/get", methods=["POST"])
# def chat():
#     try:
#         question = request.form["msg"].strip()
#         if not question:
#             return "Please ask a question."

#         session_id = get_or_create_session_id()

#         # Load last MAX_HISTORY exchanges from DB
#         history = get_history(session_id, limit=MAX_HISTORY)

#         # Enrich query for better Pinecone retrieval on follow-ups
#         retrieval_query = build_context_aware_query(question, history)
#         docs = retriever.invoke(retrieval_query)
#         context = "\n\n".join(doc.page_content for doc in docs)

#         history_text = format_history_for_prompt(history)

#         full_prompt = f"""{system_prompt}

# ---

# CONVERSATION HISTORY (use this for follow-up questions):
# {history_text}

# ---

# RELEVANT MEDICAL CONTEXT (from knowledge base):
# {context}

# ---

# CURRENT USER QUESTION:
# {question}

# ---

# INSTRUCTIONS:
# - If the question is a follow-up, refer back to the previous topic in conversation history.
# - Use the medical context to answer accurately.
# - If the answer is truly not available, say "I don't have enough information on that."
# - Be concise and clear.

# ANSWER:"""

#         answer = llm.invoke(full_prompt).content.strip()

#         # Persist to DB
#         save_message(session_id, question, answer)

#         return answer

#     except Exception:
#         traceback.print_exc()
#         return "Something went wrong. Please try again."


# @app.route("/clear")
# def clear():
#     session_id = get_or_create_session_id()
#     clear_history(session_id)
#     return "Conversation cleared."


# @app.route("/history")
# def history():
#     """Optional: view full chat history for current session (useful for debugging)."""
#     session_id = get_or_create_session_id()
#     chats = get_history(session_id, limit=50)
#     return {"session_id": session_id, "history": chats}


# # ── ENTRY POINT ───────────────────────────────────────────────
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080, debug=True)

# from flask import Flask, render_template, request, session, jsonify
# from dotenv import load_dotenv
# import os
# import traceback
# import uuid
# import time

# from src.helper import download_hugging_face_embeddings
# from src.prompt import system_prompt
# from langchain_pinecone import PineconeVectorStore
# from langchain_google_genai import ChatGoogleGenerativeAI
# from db import init_db, save_message, get_history, clear_history

# # ── ENV ───────────────────────────────────────────────────────
# load_dotenv()

# PINECONE_API_KEY = os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
# GEMINI_API_KEY   = os.environ["GEMINI_API_KEY"]   = os.getenv("GEMINI_API_KEY")

# # ── FLASK ─────────────────────────────────────────────────────
# app = Flask(__name__)
# app.secret_key = os.getenv("FLASK_SECRET_KEY", "medical_chatbot_secret")

# # ── DB INIT ───────────────────────────────────────────────────
# init_db()

# # ── RAG SETUP ─────────────────────────────────────────────────
# embeddings = download_hugging_face_embeddings()

# retriever = PineconeVectorStore.from_existing_index(
#     index_name="medical-chatbot",
#     embedding=embeddings
# ).as_retriever(search_type="similarity", search_kwargs={"k": 3})

# # ── LLM ───────────────────────────────────────────────────────
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash-lite",
#     google_api_key=GEMINI_API_KEY,
#     temperature=0.3
# )

# # ── CONSTANTS ─────────────────────────────────────────────────
# MAX_HISTORY  = 5
# MAX_RETRIES  = 3
# RETRY_WAIT   = 35   # seconds — Gemini 429 retry hint

# # ── LLM WITH RETRY ────────────────────────────────────────────
# def invoke_with_retry(prompt: str) -> str:
#     """Call LLM with automatic retry on 429 rate-limit errors."""
#     for attempt in range(MAX_RETRIES):
#         try:
#             return llm.invoke(prompt).content.strip()
#         except Exception as e:
#             err = str(e)
#             if "429" in err and attempt < MAX_RETRIES - 1:
#                 time.sleep(RETRY_WAIT)
#             else:
#                 raise

# # ── SESSION HELPERS ───────────────────────────────────────────
# def get_or_create_session_id() -> str:
#     if "session_id" not in session:
#         session["session_id"] = str(uuid.uuid4())
#     return session["session_id"]

# # ── PROMPT HELPERS ────────────────────────────────────────────
# def format_history_for_prompt(history: list) -> str:
#     if not history:
#         return "No previous conversation."
#     return "".join(
#         f"User: {h['user']}\nAssistant: {h['assistant']}\n\n"
#         for h in history
#     )

# def build_context_aware_query(question: str, history: list) -> str:
#     """Enrich short follow-up questions with last topic for better Pinecone retrieval."""
#     if len(question.split()) <= 6 and history:
#         return f"{history[-1]['user']} {question}"
#     return question

# # ── ROUTES ────────────────────────────────────────────────────
# @app.route("/")
# def home():
#     get_or_create_session_id()
#     return render_template("chat.html")


# @app.route("/get", methods=["POST"])
# def chat():
#     try:
#         question = request.form.get("msg", "").strip()
#         if not question:
#             return "Please ask a question."
#         if len(question) > 500:
#             return "Please keep your question under 500 characters."

#         session_id = get_or_create_session_id()
#         history    = get_history(session_id, limit=MAX_HISTORY)

#         # Enrich short follow-ups before hitting Pinecone
#         retrieval_query = build_context_aware_query(question, history)
#         docs    = retriever.invoke(retrieval_query)
#         context = "\n\n".join(doc.page_content for doc in docs)

#         full_prompt = f"""{system_prompt}

# ---

# CONVERSATION HISTORY (use for follow-up questions):
# {format_history_for_prompt(history)}

# ---

# RELEVANT MEDICAL CONTEXT (from knowledge base):
# {context}

# ---

# CURRENT USER QUESTION:
# {question}

# ---

# INSTRUCTIONS:
# - If the question is a follow-up, refer back to the previous topic in history.
# - Answer using the medical context provided.
# - If the answer is not available, say "I don't have enough information on that."
# - Be concise and clear.

# ANSWER:"""

#         answer = invoke_with_retry(full_prompt)
#         save_message(session_id, question, answer)
#         return answer

#     except Exception:
#         traceback.print_exc()
#         return "Something went wrong. Please try again in a moment."


# @app.route("/clear")
# def clear():
#     session_id = get_or_create_session_id()
#     clear_history(session_id)
#     return "Conversation cleared."


# @app.route("/history")
# def history():
#     session_id = get_or_create_session_id()
#     chats = get_history(session_id, limit=50)
#     return jsonify({"session_id": session_id, "history": chats})


# @app.route("/health")
# def health():
#     """Render health check endpoint."""
#     return jsonify({"status": "ok"}), 200


# # ── ENTRY POINT ───────────────────────────────────────────────
# if __name__ == '__main__':
   
#     # Read the port assigned by Render, defaulting to 5000 if running locally
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port, debug=False)


# from flask import Flask, render_template, request, session, jsonify
# from dotenv import load_dotenv
# import os
# import traceback
# import uuid
# import time

# # Direct import to match your 768-dimension uploaded vector store structur
# from src.prompt import system_prompt
# from langchain_pinecone import PineconeVectorStore
# from langchain_google_genai import ChatGoogleGenerativeAI
# from db import init_db, save_message, get_history, clear_history

# # ── 1. ENV CONFIGURATION ──────────────────────────────────────
# load_dotenv()

# PINECONE_API_KEY = os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
# GEMINI_API_KEY   = os.environ["GEMINI_API_KEY"]   = os.getenv("GEMINI_API_KEY")

# # ── 2. FLASK APP SETUP ────────────────────────────────────────
# app = Flask(__name__)
# app.secret_key = os.getenv("FLASK_SECRET_KEY", "medical_chatbot_secret")

# # Initialize the local SQLite chat database
# init_db()

# # ── 3. RAG KNOWLEDGE BASE SETUP ───────────────────────────────
# # Must match the exact model weights used during ingestion!
# # ── 3. RAG KNOWLEDGE BASE SETUP ───────────────────────────────
# # We completely bypass local embedding declarations to keep things lightweight!
# retriever = PineconeVectorStore.from_existing_index(
#     index_name="medical-chatbot",
#     embedding=None  
# ).as_retriever(search_type="similarity", search_kwargs={"k": 3})
# # ── 4. LLM CONFIGURATION ──────────────────────────────────────
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash-lite",
#     google_api_key=GEMINI_API_KEY,
#     temperature=0.3
# )

# # ── 5. CONSTANTS & RETRY LOGIC ────────────────────────────────
# MAX_HISTORY  = 5
# MAX_RETRIES  = 3
# RETRY_WAIT   = 35   # seconds — Gemini 429 rate limit cooling window

# def invoke_with_retry(prompt: str) -> str:
#     """Call LLM with automatic fallback retry handling on 429 rate limits."""
#     for attempt in range(MAX_RETRIES):
#         try:
#             return llm.invoke(prompt).content.strip()
#         except Exception as e:
#             err = str(e)
#             if "429" in err and attempt < MAX_RETRIES - 1:
#                 time.sleep(RETRY_WAIT)
#             else:
#                 raise

# # ── 6. CONVERSATION STATE HELPERS ─────────────────────────────
# def get_or_create_session_id() -> str:
#     if "session_id" not in session:
#         session["session_id"] = str(uuid.uuid4())
#     return session["session_id"]

# def format_history_for_prompt(history: list) -> str:
#     if not history:
#         return "No previous conversation."
#     return "".join(
#         f"User: {h['user']}\nAssistant: {h['assistant']}\n\n"
#         for h in history
#     )

# def build_context_aware_query(question: str, history: list) -> str:
#     """Enrich short contextless follow-up queries before looking up Pinecone."""
#     if len(question.split()) <= 6 and history:
#         return f"{history[-1]['user']} {question}"
#     return question

# # ── 7. APPLICATION ENDPOINTS ──────────────────────────────────
# @app.route("/")
# def home():
#     get_or_create_session_id()
#     return render_template("chat.html")


# @app.route("/get", methods=["POST"])
# def chat():
#     try:
#         question = request.form.get("msg", "").strip()
#         if not question:
#             return "Please ask a question."
#         if len(question) > 500:
#             return "Please keep your question under 500 characters."

#         session_id = get_or_create_session_id()
#         history    = get_history(session_id, limit=MAX_HISTORY)

#         # Optimize short queries using history context before querying vector spaces
#         retrieval_query = build_context_aware_query(question, history)
#         docs    = retriever.invoke(retrieval_query)
#         context = "\n\n".join(doc.page_content for doc in docs)

#         full_prompt = f"""{system_prompt}

# ---

# CONVERSATION HISTORY (use for follow-up questions):
# {format_history_for_prompt(history)}

# ---

# RELEVANT MEDICAL CONTEXT (from knowledge base):
# {context}

# ---

# CURRENT USER QUESTION:
# {question}

# ---

# INSTRUCTIONS:
# - If the question is a follow-up, refer back to the previous topic in history.
# - Answer using the medical context provided.
# - If the answer is not available, say "I don't have enough information on that."
# - Be concise and clear.

# ANSWER:"""

#         answer = invoke_with_retry(full_prompt)
#         save_message(session_id, question, answer)
#         return answer

#     except Exception:
#         traceback.print_exc()
#         return "Something went wrong. Please try again in a moment."


# @app.route("/clear")
# def clear():
#     session_id = get_or_create_session_id()
#     clear_history(session_id)
#     return "Conversation cleared."


# @app.route("/history")
# def history():
#     session_id = get_or_create_session_id()
#     chats = get_history(session_id, limit=50)
#     return jsonify({"session_id": session_id, "history": chats})


# @app.route("/health")
# def health():
#     """System health check diagnostic hook."""
#     return jsonify({"status": "ok"}), 200


# # ── 8. SYSTEM ENTRY POINT ─────────────────────────────────────
# if __name__ == '__main__':
#     # Dynamically bind ports for production container services (Render/Heroku)
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port, debug=False)


from flask import Flask, render_template, request, session, jsonify
from dotenv import load_dotenv
import os
import traceback
import uuid
import time

from src.prompt import system_prompt
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from db import init_db, save_message, get_history, clear_history

# ── 1. ENV CONFIGURATION ──────────────────────────────────────
load_dotenv()

PINECONE_API_KEY = os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY   = os.environ["GEMINI_API_KEY"]   = os.getenv("GEMINI_API_KEY")

# ── 2. FLASK APP SETUP ────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "medical_chatbot_secret")

# Initialize the local SQLite chat database
init_db()

# ── 3. RAG KNOWLEDGE BASE SETUP ───────────────────────────────
# We completely bypass local embedding declarations to keep things lightweight!
retriever = PineconeVectorStore.from_existing_index(
    index_name="medical-chatbot",
    embedding=None  
).as_retriever(search_type="similarity", search_kwargs={"k": 3})

# ── 4. LLM CONFIGURATION ──────────────────────────────────────
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=GEMINI_API_KEY,
    temperature=0.3
)

# ── 5. CONSTANTS & RETRY LOGIC ────────────────────────────────
MAX_HISTORY  = 5
MAX_RETRIES  = 3
RETRY_WAIT   = 35   # seconds — Gemini 429 rate limit cooling window

def invoke_with_retry(prompt: str) -> str:
    """Call LLM with automatic fallback retry handling on 429 rate limits."""
    for attempt in range(MAX_RETRIES):
        try:
            return llm.invoke(prompt).content.strip()
        except Exception as e:
            err = str(e)
            if "429" in err and attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_WAIT)
            else:
                raise

# ── 6. CONVERSATION STATE HELPERS ─────────────────────────────
def get_or_create_session_id() -> str:
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return session["session_id"]

def format_history_for_prompt(history: list) -> str:
    if not history:
        return "No previous conversation."
    return "".join(
        f"User: {h['user']}\nAssistant: {h['assistant']}\n\n"
        for h in history
    )

def build_context_aware_query(question: str, history: list) -> str:
    """Enrich short contextless follow-up queries before looking up Pinecone."""
    if len(question.split()) <= 6 and history:
        return f"{history[-1]['user']} {question}"
    return question

# ── 7. APPLICATION ENDPOINTS ──────────────────────────────────
@app.route("/")
def home():
    get_or_create_session_id()
    return render_template("chat.html")


@app.route("/get", methods=["POST"])
def chat():
    try:
        question = request.form.get("msg", "").strip()
        if not question:
            return "Please ask a question."
        if len(question) > 500:
            return "Please keep your question under 500 characters."

        session_id = get_or_create_session_id()
        history    = get_history(session_id, limit=MAX_HISTORY)

        # Optimize short queries using history context before querying vector spaces
        retrieval_query = build_context_aware_query(question, history)
        docs    = retriever.invoke(retrieval_query)
        context = "\n\n".join(doc.page_content for doc in docs)

        full_prompt = f"""{system_prompt}

---

CONVERSATION HISTORY (use for follow-up questions):
{format_history_for_prompt(history)}

---

RELEVANT MEDICAL CONTEXT (from knowledge base):
{context}

---

CURRENT USER QUESTION:
{question}

---

INSTRUCTIONS:
- If the question is a follow-up, refer back to the previous topic in history.
- Answer using the medical context provided.
- If the answer is not available, say "I don't have enough information on that."
- Be concise and clear.

ANSWER:"""

        answer = invoke_with_retry(full_prompt)
        save_message(session_id, question, answer)
        return answer

    except Exception:
        traceback.print_exc()
        return "Something went wrong. Please try again in a moment."


@app.route("/clear")
def clear():
    session_id = get_or_create_session_id()
    clear_history(session_id)
    return "Conversation cleared."


@app.route("/history")
def history():
    session_id = get_or_create_session_id()
    chats = get_history(session_id, limit=50)
    return jsonify({"session_id": session_id, "history": chats})


@app.route("/health")
def health():
    """System health check diagnostic hook."""
    return jsonify({"status": "ok"}), 200


# ── 8. SYSTEM ENTRY POINT ─────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)