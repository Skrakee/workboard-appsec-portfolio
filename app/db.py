"""SQLite storage and synthetic workspace data."""
import hashlib
import os
import secrets
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = lambda: os.environ.get("DB_PATH", "/tmp/appsec-workboard.sqlite3")

@contextmanager
def connect():
    path = DB_PATH()
    if path != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def password_hash(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 260_000)
    return f"{salt.hex()}:{digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        salt, wanted = stored.split(":", 1)
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 260_000)
        return secrets.compare_digest(actual, bytes.fromhex(wanted))
    except (ValueError, TypeError):
        return False


def init_db():
    with connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE,
          password_hash TEXT NOT NULL, org_id INTEGER NOT NULL,
          role TEXT NOT NULL CHECK(role IN ('admin','member'))
        );
        CREATE TABLE IF NOT EXISTS docs (
          id INTEGER PRIMARY KEY, org_id INTEGER NOT NULL,
          owner_id INTEGER NOT NULL REFERENCES users(id),
          title TEXT NOT NULL, content TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS comments (
          id INTEGER PRIMARY KEY, doc_id INTEGER NOT NULL REFERENCES docs(id),
          author_id INTEGER NOT NULL REFERENCES users(id), body TEXT NOT NULL
        );
        """)
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if count:
            return
        users = [
            (1, "admin@atlas.test", "AtlasAdmin123!", 1, "admin"),
            (2, "member@atlas.test", "AtlasMember123!", 1, "member"),
            (3, "admin@boreal.test", "BorealAdmin123!", 2, "admin"),
            (4, "member@boreal.test", "BorealMember123!", 2, "member"),
        ]
        for user_id, email, pwd, org_id, role in users:
            conn.execute("INSERT INTO users VALUES(?,?,?,?,?)", (user_id, email, password_hash(pwd), org_id, role))
        conn.executemany("INSERT INTO docs(id, org_id, owner_id, title, content) VALUES(?,?,?,?,?)", [
            (101, 1, 2, "Atlas - Q4 Plan", "Atlas internal planning draft"),
            (102, 1, 1, "Atlas - Budget", "Atlas budget placeholders"),
            (201, 2, 4, "Boreal - Project Notes", "Boreal private notes"),
            (202, 2, 3, "Boreal - Roadmap", "Boreal roadmap draft"),
        ])
        conn.execute("INSERT INTO comments(doc_id, author_id, body) VALUES(101,2,'Initial draft looks good')")
