

# # from flask import Flask, render_template, request, session, jsonify
# # from dotenv import load_dotenv
# # from langchain_google_genai import ChatGoogleGenerativeAI
# # from db import init_db, save_message, get_history, clear_history
# # from src.prompt import system_prompt
# # from pinecone import Pinecone
# # from sentence_transformers import SentenceTransformer
# # import os, traceback, uuid, time

# # # ── ENV ───────────────────────────────────────────────────────
# # load_dotenv()
# # PINECONE_API_KEY = os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
# # GEMINI_API_KEY   = os.environ["GEMINI_API_KEY"]   = os.getenv("GEMINI_API_KEY")

# # # ── FLASK ─────────────────────────────────────────────────────
# # app = Flask(__name__)
# # app.secret_key = os.getenv("FLASK_SECRET_KEY", "medical_chatbot_secret")
# # init_db()

# # # ── EMBEDDING MODEL (loaded once at startup, ~420MB) ──────────
# # # On Render: use a lightweight model to save RAM
# # MODEL_NAME = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-mpnet-base-v2")
# # print(f"Loading embedding model: {MODEL_NAME}")
# # embed_model = SentenceTransformer(MODEL_NAME)
# # print("Embedding model ready.")

# # # ── PINECONE ──────────────────────────────────────────────────
# # pc    = Pinecone(api_key=PINECONE_API_KEY)
# # index = pc.Index("medical-chatbot")

# # # ── LLM ───────────────────────────────────────────────────────
# # llm = ChatGoogleGenerativeAI(
# #     model="gemini-2.5-flash-lite",
# #     google_api_key=GEMINI_API_KEY,
# #     temperature=0.3
# # )

# # MAX_HISTORY = 5
# # MAX_RETRIES = 3
# # RETRY_WAIT  = 35

# # def invoke_with_retry(prompt: str) -> str:
# #     for attempt in range(MAX_RETRIES):
# #         try:
# #             return llm.invoke(prompt).content.strip()
# #         except Exception as e:
# #             if "429" in str(e) and attempt < MAX_RETRIES - 1:
# #                 time.sleep(RETRY_WAIT)
# #             else:
# #                 raise

# # def get_or_create_session_id() -> str:
# #     if "session_id" not in session:
# #         session["session_id"] = str(uuid.uuid4())
# #     return session["session_id"]

# # def format_history(history: list) -> str:
# #     if not history:
# #         return "No previous conversation."
# #     return "".join(
# #         f"User: {h['user']}\nAssistant: {h['assistant']}\n\n"
# #         for h in history
# #     )

# # def enrich_query(question: str, history: list) -> str:
# #     if len(question.split()) <= 6 and history:
# #         return f"{history[-1]['user']} {question}"
# #     return question

# # def get_context(query: str) -> str:
# #     vector = embed_model.encode(query).tolist()
# #     result = index.query(vector=vector, top_k=3, include_metadata=True)
# #     chunks = [
# #         m["metadata"].get("text", "")
# #         for m in result.get("matches", [])
# #         if m.get("metadata", {}).get("text")
# #     ]
# #     return "\n\n".join(chunks)

# # @app.route("/")
# # def home():
# #     get_or_create_session_id()
# #     return render_template("chat.html")

# # @app.route("/get", methods=["POST"])
# # def chat():
# #     try:
# #         question = request.form.get("msg", "").strip()
# #         if not question:
# #             return "Please ask a question."
# #         if len(question) > 500:
# #             return "Please keep your question under 500 characters."

# #         session_id = get_or_create_session_id()
# #         history    = get_history(session_id, limit=MAX_HISTORY)
# #         context    = get_context(enrich_query(question, history))

# #         full_prompt = f"""{system_prompt}

# # ---

# # CONVERSATION HISTORY (use for follow-up questions):
# # {format_history(history)}

# # ---

# # RELEVANT MEDICAL CONTEXT (from knowledge base):
# # {context}

# # ---

# # CURRENT USER QUESTION:
# # {question}

# # ---

# # INSTRUCTIONS:
# # - If the question is a follow-up, refer back to the previous topic in history.
# # - Answer using the medical context provided.
# # - If the answer is not available, say "I don't have enough information on that."
# # - Be concise and clear.

# # ANSWER:"""

# #         answer = invoke_with_retry(full_prompt)
# #         save_message(session_id, question, answer)
# #         return answer

# #     except Exception:
# #         traceback.print_exc()
# #         return "Something went wrong. Please try again in a moment."

# # @app.route("/clear")
# # def clear():
# #     clear_history(get_or_create_session_id())
# #     return "Conversation cleared."

# # @app.route("/history")
# # def history():
# #     chats = get_history(get_or_create_session_id(), limit=50)
# #     return jsonify({"history": chats})

# # @app.route("/health")
# # def health():
# #     return jsonify({"status": "ok"}), 200

# # if __name__ == "__main__":
# #     port = int(os.environ.get("PORT", 5000))
# #     app.run(host="0.0.0.0", port=port, debug=False)



# from flask import Flask, render_template, request, session, jsonify
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from db import init_db, save_message, get_history, clear_history
# from src.prompt import system_prompt
# from pinecone import Pinecone
# import os, traceback, uuid, time

# # ── ENV ───────────────────────────────────────────────────────
# load_dotenv()
# PINECONE_API_KEY = os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
# GEMINI_API_KEY   = os.environ["GEMINI_API_KEY"]   = os.getenv("GEMINI_API_KEY")

# # ── FLASK ─────────────────────────────────────────────────────
# app = Flask(__name__)
# app.secret_key = os.getenv("FLASK_SECRET_KEY", "medical_chatbot_secret")
# init_db()

# # ── EMBEDDINGS — no torch, CPU only ───────────────────────────
# # Uses ONNX runtime backend: ~80MB RAM vs torch's 1.5GB
# print("Loading embedding model...")
# os.environ["TOKENIZERS_PARALLELISM"] = "false"

# from sentence_transformers import SentenceTransformer
# embed_model = SentenceTransformer(
#     "sentence-transformers/all-mpnet-base-v2",
#     backend="onnx",          # skip torch entirely
#     model_kwargs={"file_name": "onnx/model.onnx"}
# )
# print("Embedding model ready.")

# # ── PINECONE ──────────────────────────────────────────────────
# pc    = Pinecone(api_key=PINECONE_API_KEY)
# index = pc.Index("medical-chatbot")

# # ── LLM ───────────────────────────────────────────────────────
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash-lite",
#     google_api_key=GEMINI_API_KEY,
#     temperature=0.3
# )

# MAX_HISTORY = 5
# MAX_RETRIES = 3
# RETRY_WAIT  = 35

# def invoke_with_retry(prompt: str) -> str:
#     for attempt in range(MAX_RETRIES):
#         try:
#             return llm.invoke(prompt).content.strip()
#         except Exception as e:
#             if "429" in str(e) and attempt < MAX_RETRIES - 1:
#                 time.sleep(RETRY_WAIT)
#             else:
#                 raise

# def get_or_create_session_id() -> str:
#     if "session_id" not in session:
#         session["session_id"] = str(uuid.uuid4())
#     return session["session_id"]

# def format_history(history: list) -> str:
#     if not history:
#         return "No previous conversation."
#     return "".join(
#         f"User: {h['user']}\nAssistant: {h['assistant']}\n\n"
#         for h in history
#     )

# def enrich_query(question: str, history: list) -> str:
#     if len(question.split()) <= 6 and history:
#         return f"{history[-1]['user']} {question}"
#     return question

# def get_context(query: str) -> str:
#     vector = embed_model.encode(query).tolist()
#     result = index.query(vector=vector, top_k=3, include_metadata=True)
#     chunks = [
#         m["metadata"].get("text", "")
#         for m in result.get("matches", [])
#         if m.get("metadata", {}).get("text")
#     ]
#     return "\n\n".join(chunks)

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
#         context    = get_context(enrich_query(question, history))

#         full_prompt = f"""{system_prompt}

# ---

# CONVERSATION HISTORY (use for follow-up questions):
# {format_history(history)}

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
#     clear_history(get_or_create_session_id())
#     return "Conversation cleared."

# @app.route("/history")
# def history():
#     chats = get_history(get_or_create_session_id(), limit=50)
#     return jsonify({"history": chats})

# @app.route("/health")
# def health():
#     return jsonify({"status": "ok"}), 200

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port, debug=False)


from flask import Flask, render_template, request, session, jsonify
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from db import init_db, save_message, get_history, clear_history
from src.prompt import system_prompt
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import os, traceback, uuid, time

load_dotenv()
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY   = os.environ["GEMINI_API_KEY"]   = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "medical_chatbot_secret")
init_db()

os.environ["TOKENIZERS_PARALLELISM"] = "false"
print("Loading embedding model...")
embed_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
print("Embedding model ready.")

pc    = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("medical-chatbot")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=GEMINI_API_KEY,
    temperature=0.3
)

MAX_HISTORY = 5
MAX_RETRIES = 3
RETRY_WAIT  = 35

def invoke_with_retry(prompt):
    for attempt in range(MAX_RETRIES):
        try:
            return llm.invoke(prompt).content.strip()
        except Exception as e:
            if "429" in str(e) and attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_WAIT)
            else:
                raise

def get_or_create_session_id():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return session["session_id"]

def format_history(history):
    if not history:
        return "No previous conversation."
    return "".join(f"User: {h['user']}\nAssistant: {h['assistant']}\n\n" for h in history)

def enrich_query(question, history):
    if len(question.split()) <= 6 and history:
        return f"{history[-1]['user']} {question}"
    return question

def get_context(query):
    vector = embed_model.encode(query).tolist()
    result = index.query(vector=vector, top_k=3, include_metadata=True)
    return "\n\n".join(
        m["metadata"].get("text", "")
        for m in result.get("matches", [])
        if m.get("metadata", {}).get("text")
    )

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
        context    = get_context(enrich_query(question, history))

        full_prompt = f"""{system_prompt}

---
CONVERSATION HISTORY:
{format_history(history)}

---
RELEVANT MEDICAL CONTEXT:
{context}

---
CURRENT USER QUESTION:
{question}

---
INSTRUCTIONS:
- If follow-up, refer back to previous topic in history.
- Answer using the medical context provided.
- If not available, say "I don't have enough information on that."
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
    clear_history(get_or_create_session_id())
    return "Conversation cleared."

@app.route("/history")
def history():
    return jsonify({"history": get_history(get_or_create_session_id(), limit=50)})

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)