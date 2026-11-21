def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"

def test_login_invalid_password(client):
    r = client.post("/api/auth/login", json={"email": "member@atlas.test", "password": "nope"})
    assert r.status_code == 401

def test_login_and_profile(client, login_as):
    h = login_as("member@atlas.test", "AtlasMember123!")
    r = client.get("/api/me", headers=h)
    assert r.status_code == 200 and r.json()["org_id"] == 1

def test_list_docs_is_org_scoped(client, login_as):
    h = login_as("member@atlas.test", "AtlasMember123!")
    r = client.get("/api/docs", headers=h)
    assert r.status_code == 200
    assert {d["id"] for d in r.json()} == {101,102}

def test_non_admin_cannot_update_doc(client, login_as):
    h = login_as("member@atlas.test", "AtlasMember123!")
    r = client.patch("/api/docs/101", json={"title":"changed"}, headers=h)
    assert r.status_code == 403

def test_comment_roundtrip(client, login_as):
    h = login_as("member@atlas.test", "AtlasMember123!")
    r = client.post("/api/docs/101/comments", json={"body":"Looks fine"}, headers=h)
    assert r.status_code == 201
    r = client.get("/api/docs/101/comments", headers=h)
    assert r.status_code == 200 and any(c["body"] == "Looks fine" for c in r.json())

def test_comments_cross_org_are_denied(client, login_as):
    h = login_as("member@atlas.test", "AtlasMember123!")
    assert client.get("/api/docs/201/comments", headers=h).status_code == 404

def test_unauthenticated_request_denied(client):
    assert client.get("/api/docs").status_code == 401
