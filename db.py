# """
# db.py — Chat history persistence layer
# --------------------------------------
# Default: SQLite  (no setup needed, file-based)
# Switch:  PostgreSQL or MongoDB — see comments at bottom
# """

# import sqlite3
# import os
# from datetime import datetime

# DB_PATH = os.getenv("SQLITE_DB_PATH", "chat_history.db")

# # ── INIT ──────────────────────────────────────────────────────
# def init_db() -> None:
#     """Create the chat_history table if it doesn't exist."""
#     with _get_conn() as conn:
#         conn.execute("""
#             CREATE TABLE IF NOT EXISTS chat_history (
#                 id          INTEGER PRIMARY KEY AUTOINCREMENT,
#                 session_id  TEXT    NOT NULL,
#                 user_msg    TEXT    NOT NULL,
#                 bot_reply   TEXT    NOT NULL,
#                 created_at  TEXT    NOT NULL
#             )
#         """)
#         conn.execute("""
#             CREATE INDEX IF NOT EXISTS idx_session
#             ON chat_history (session_id, created_at)
#         """)

# # ── CONNECTION ────────────────────────────────────────────────
# def _get_conn() -> sqlite3.Connection:
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row   # lets us access columns by name
#     return conn

# # ── WRITE ─────────────────────────────────────────────────────
# def save_message(session_id: str, user_msg: str, bot_reply: str) -> None:
#     """Insert one exchange into the database."""
#     with _get_conn() as conn:
#         conn.execute("""
#             INSERT INTO chat_history (session_id, user_msg, bot_reply, created_at)
#             VALUES (?, ?, ?, ?)
#         """, (session_id, user_msg, bot_reply, datetime.utcnow().isoformat()))

# # ── READ ──────────────────────────────────────────────────────
# def get_history(session_id: str, limit: int = 5) -> list[dict]:
#     """
#     Return the last `limit` exchanges for this session,
#     oldest-first so the prompt reads naturally.
#     """
#     with _get_conn() as conn:
#         rows = conn.execute("""
#             SELECT user_msg, bot_reply FROM chat_history
#             WHERE session_id = ?
#             ORDER BY created_at DESC
#             LIMIT ?
#         """, (session_id, limit)).fetchall()

#     # Reverse so oldest exchange comes first in the prompt
#     return [{"user": r["user_msg"], "assistant": r["bot_reply"]}
#             for r in reversed(rows)]

# # ── DELETE ────────────────────────────────────────────────────
# def clear_history(session_id: str) -> None:
#     """Delete all messages for a session (called by /clear route)."""
#     with _get_conn() as conn:
#         conn.execute("""
#             DELETE FROM chat_history WHERE session_id = ?
#         """, (session_id,))

# ─────────────────────────────────────────────────────────────
# HOW TO SWITCH TO POSTGRESQL (when deploying)
# ─────────────────────────────────────────────────────────────
# pip install psycopg2-binary
#
# Replace _get_conn() with:
#   import psycopg2, psycopg2.extras
#   def _get_conn():
#       return psycopg2.connect(os.getenv("DATABASE_URL"))
#
# Change ? placeholders to %s in all queries.
# Change INTEGER PRIMARY KEY AUTOINCREMENT → SERIAL PRIMARY KEY
# Everything else (save_message, get_history, clear_history) stays the same.
#
# ─────────────────────────────────────────────────────────────
# HOW TO SWITCH TO MONGODB
# ─────────────────────────────────────────────────────────────
# pip install pymongo
#
# from pymongo import MongoClient
# client = MongoClient(os.getenv("MONGO_URI"))
# db_mongo = client["medical_chatbot"]
# collection = db_mongo["chat_history"]
#
# def save_message(session_id, user_msg, bot_reply):
#     collection.insert_one({
#         "session_id": session_id,
#         "user_msg": user_msg,
#         "bot_reply": bot_reply,
#         "created_at": datetime.utcnow()
#     })
#
# def get_history(session_id, limit=5):
#     docs = collection.find(
#         {"session_id": session_id},
#         sort=[("created_at", -1)],
#         limit=limit
#     )
#     return [{"user": d["user_msg"], "assistant": d["bot_reply"]}
#             for d in reversed(list(docs))]
#
# def clear_history(session_id):
# #     collection.delete_many({"session_id": session_id})

# """
# db.py — Chat history persistence
# Default: SQLite (works on Render free tier — file in /tmp)
# """
# import sqlite3
# import os
# from datetime import datetime

# # Detect if running on Render, otherwise use local directory safe path
# if os.getenv("RENDER"):
#     DB_PATH = os.getenv("SQLITE_DB_PATH", "/tmp/chat_history.db")
# else:
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#     DB_PATH = os.path.join(BASE_DIR, "chat_history.db")

# # ── INIT ──────────────────────────────────────────────────────
# def init_db() -> None:
#     """Create the chat_history table if it doesn't exist."""
#     with _conn() as c:
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS chat_history (
#                 id          INTEGER PRIMARY KEY AUTOINCREMENT,
#                 session_id  TEXT    NOT NULL,
#                 user_msg    TEXT    NOT NULL,
#                 bot_reply   TEXT    NOT NULL,
#                 created_at  TEXT    NOT NULL
#             )
#         """)
#         c.execute("""
#             CREATE INDEX IF NOT EXISTS idx_session
#             ON chat_history (session_id, created_at)
#         """)

# # ── CONNECTION ────────────────────────────────────────────────
# def _conn() -> sqlite3.Connection:
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row   # lets us access columns by name
#     return conn

# # ── WRITE ─────────────────────────────────────────────────────
# def save_message(session_id: str, user_msg: str, bot_reply: str) -> None:
#     """Insert one exchange into the database."""
#     with _conn() as c:
#         c.execute("""
#             INSERT INTO chat_history (session_id, user_msg, bot_reply, created_at)
#             VALUES (?, ?, ?, ?)
#         """, (session_id, user_msg, bot_reply, datetime.utcnow().isoformat()))

# # ── READ ──────────────────────────────────────────────────────
# def get_history(session_id: str, limit: int = 5) -> list[dict]:
#     """
#     Return the last `limit` exchanges for this session,
#     oldest-first so the prompt reads naturally.
#     """
#     with _conn() as c:
#         rows = c.execute("""
#             SELECT user_msg, bot_reply FROM chat_history
#             WHERE session_id = ?
#             ORDER BY created_at DESC LIMIT ?
#         """, (session_id, limit)).fetchall()
#     return [{"user": r["user_msg"], "assistant": r["bot_reply"]}
#             for r in reversed(rows)]

# # ── DELETE ────────────────────────────────────────────────────
# def clear_history(session_id: str) -> None:
#     """Delete all messages for a session (called by /clear route)."""
#     with _conn() as c:
#         c.execute("DELETE FROM chat_history WHERE session_id = ?", (session_id,))










"""
db.py — SQLite chat history
Works locally (saves next to app) and on Render (/tmp)
"""
import sqlite3, os
from datetime import datetime

# /tmp on Render (ephemeral), local dir otherwise
DB_PATH = "/tmp/chat_history.db" if os.getenv("RENDER") else \
          os.path.join(os.path.dirname(os.path.abspath(__file__)), "chat_history.db")

def init_db() -> None:
    with _conn() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_msg   TEXT NOT NULL,
                bot_reply  TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        c.execute("""
            CREATE INDEX IF NOT EXISTS idx_session
            ON chat_history (session_id, created_at)
        """)

def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def save_message(session_id: str, user_msg: str, bot_reply: str) -> None:
    with _conn() as c:
        c.execute("""
            INSERT INTO chat_history (session_id, user_msg, bot_reply, created_at)
            VALUES (?, ?, ?, ?)
        """, (session_id, user_msg, bot_reply, datetime.utcnow().isoformat()))

def get_history(session_id: str, limit: int = 5) -> list[dict]:
    with _conn() as c:
        rows = c.execute("""
            SELECT user_msg, bot_reply FROM chat_history
            WHERE session_id = ?
            ORDER BY created_at DESC LIMIT ?
        """, (session_id, limit)).fetchall()
    return [{"user": r["user_msg"], "assistant": r["bot_reply"]}
            for r in reversed(rows)]

def clear_history(session_id: str) -> None:
    with _conn() as c:
        c.execute("DELETE FROM chat_history WHERE session_id = ?", (session_id,))