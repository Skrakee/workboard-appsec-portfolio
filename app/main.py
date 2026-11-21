"""Workboard: a small, deliberately imperfect local AppSec training application.

SECURITY NOTE: Contains intentional vulnerabilities for controlled, local testing.
See SECURITY_SCOPE.md. Never expose this app to the Internet.
"""
import os
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path

import jwt
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from datetime import datetime, timedelta, timezone

from .db import connect, init_db, verify_password

SECRET = os.environ.get("APP_SECRET", "local-only-training-secret-change-before-deploying-2026")
AUTH = HTTPBearer(auto_error=False)
STATIC_DIR = Path(__file__).resolve().parent / "static"

@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Workboard AppSec Portfolio Lab", version="0.1.0", lifespan=lifespan)

class LoginRequest(BaseModel):
    email: str
    password: str

class DocUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, max_length=4000)

class CommentCreate(BaseModel):
    body: str = Field(min_length=1, max_length=1000)


def current_user(auth: HTTPAuthorizationCredentials | None = Depends(AUTH)):
    if auth is None or auth.scheme.lower() != "bearer":
        raise HTTPException(401, "Authentication required")
    try:
        claims = jwt.decode(auth.credentials, SECRET, algorithms=["HS256"])
        user_id = int(claims["sub"])
    except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
        raise HTTPException(401, "Invalid or expired token")
    with connect() as conn:
        user = conn.execute("SELECT id,email,org_id,role FROM users WHERE id=?", (user_id,)).fetchone()
    if user is None:
        raise HTTPException(401, "Unknown account")
    return dict(user)


def get_doc(conn, doc_id):
    doc = conn.execute("SELECT * FROM docs WHERE id=?", (doc_id,)).fetchone()
    if doc is None:
        raise HTTPException(404, "Document not found")
    return dict(doc)

@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/static/app.js")
def js_file():
    return FileResponse(STATIC_DIR / "app.js", media_type="text/javascript")

@app.get("/static/style.css")
def css_file():
    return FileResponse(STATIC_DIR / "style.css", media_type="text/css")

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/auth/login")
def login(body: LoginRequest):
    with connect() as conn:
        user = conn.execute("SELECT * FROM users WHERE email=?", (body.email,)).fetchone()
    if user is None or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(401, "Invalid credentials")
    exp = datetime.now(timezone.utc) + timedelta(hours=1)
    token = jwt.encode({"sub": str(user["id"]), "exp": exp}, SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/me")
def me(user=Depends(current_user)):
    return user

@app.get("/api/docs")
def list_docs(user=Depends(current_user)):
    with connect() as conn:
        docs = conn.execute("SELECT * FROM docs WHERE org_id=? ORDER BY id", (user["org_id"],)).fetchall()
    return [dict(d) for d in docs]

# Keep this route before /api/docs/{doc_id} for readability.
@app.get("/api/docs/search")
def search_docs(q: str = Query(default="", max_length=100), user=Depends(current_user)):
    with connect() as conn:
        # Deliberately imperfect query in this training snapshot; review in the AppSec phase.
        statement = f"SELECT * FROM docs WHERE org_id={user['org_id']} AND title LIKE '%{q}%' ORDER BY id"
        try:
            docs = conn.execute(statement).fetchall()
        except sqlite3.OperationalError:
            raise HTTPException(400, "Invalid search")
    return [dict(d) for d in docs]

@app.get("/api/docs/{doc_id}")
def read_doc(doc_id: int, user=Depends(current_user)):
    with connect() as conn:
        doc = get_doc(conn, doc_id)
        # Deliberately incomplete access policy; to be assessed during the exercise.
        return doc

@app.patch("/api/docs/{doc_id}")
def update_doc(doc_id: int, body: DocUpdate, user=Depends(current_user)):
    if user["role"] != "admin":
        raise HTTPException(403, "Admin access required")
    with connect() as conn:
        doc = get_doc(conn, doc_id)
        new_title = body.title if body.title is not None else doc["title"]
        new_content = body.content if body.content is not None else doc["content"]
        conn.execute("UPDATE docs SET title=?, content=? WHERE id=?", (new_title, new_content, doc_id))
        return get_doc(conn, doc_id)

@app.get("/api/docs/{doc_id}/comments")
def list_comments(doc_id: int, user=Depends(current_user)):
    with connect() as conn:
        doc = get_doc(conn, doc_id)
        if doc["org_id"] != user["org_id"]:
            raise HTTPException(404, "Document not found")
        rows = conn.execute("""
            SELECT c.id,c.body,u.email AS author FROM comments c
            JOIN users u ON c.author_id=u.id WHERE c.doc_id=? ORDER BY c.id
        """, (doc_id,)).fetchall()
        return [dict(r) for r in rows]

@app.post("/api/docs/{doc_id}/comments", status_code=201)
def add_comment(doc_id: int, body: CommentCreate, user=Depends(current_user)):
    with connect() as conn:
        doc = get_doc(conn, doc_id)
        if doc["org_id"] != user["org_id"]:
            raise HTTPException(404, "Document not found")
        cur = conn.execute("INSERT INTO comments(doc_id,author_id,body) VALUES(?,?,?)", (doc_id,user["id"],body.body))
        return {"id": cur.lastrowid, "doc_id": doc_id, "body": body.body}
