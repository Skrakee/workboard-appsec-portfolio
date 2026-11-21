"""Regression coverage for F-01: tenant isolation when editing documents."""

import pytest

from app.db import connect


def document_snapshot(doc_id):
    """Read stored data independently of the document-read endpoint's policy."""
    with connect() as conn:
        row = conn.execute("SELECT * FROM docs WHERE id=?", (doc_id,)).fetchone()
    assert row is not None
    return dict(row)


@pytest.mark.parametrize(
    "email,password,doc_id",
    [
        ("admin@atlas.test", "AtlasAdmin123!", 201),
        ("admin@boreal.test", "BorealAdmin123!", 101),
    ],
    ids=["atlas-cannot-edit-boreal", "boreal-cannot-edit-atlas"],
)
def test_admin_cannot_edit_another_organization(client, login_as, email, password, doc_id):
    headers = login_as(email, password)
    before = document_snapshot(doc_id)

    response = client.patch(
        f"/api/docs/{doc_id}",
        headers=headers,
        json={"title": "Unauthorized change", "content": "Must not be saved"},
    )
    after = document_snapshot(doc_id)

    # Assert both properties together so failure output includes persistence evidence.
    assert (response.status_code, after) == (404, before)


@pytest.mark.parametrize(
    "email,password,doc_id",
    [
        ("admin@atlas.test", "AtlasAdmin123!", 101),
        ("admin@boreal.test", "BorealAdmin123!", 201),
    ],
    ids=["atlas-can-edit-atlas", "boreal-can-edit-boreal"],
)
def test_admin_can_edit_own_organization(client, login_as, email, password, doc_id):
    headers = login_as(email, password)
    before = document_snapshot(doc_id)
    changes = {"title": "Updated plan", "content": "Authorized update"}

    response = client.patch(f"/api/docs/{doc_id}", headers=headers, json=changes)

    assert response.status_code == 200
    expected = {**before, **changes}
    assert response.json() == expected
    assert document_snapshot(doc_id) == expected


@pytest.mark.parametrize("doc_id", [101, 201], ids=["own-organization", "other-organization"])
def test_member_cannot_edit_documents(client, login_as, doc_id):
    headers = login_as("member@atlas.test", "AtlasMember123!")
    before = document_snapshot(doc_id)

    response = client.patch(
        f"/api/docs/{doc_id}", headers=headers, json={"title": "Forbidden change"}
    )

    assert (response.status_code, document_snapshot(doc_id)) == (403, before)


def test_unauthenticated_edit_is_denied(client):
    before = document_snapshot(101)

    response = client.patch("/api/docs/101", json={"title": "Forbidden change"})

    assert (response.status_code, document_snapshot(101)) == (401, before)


def test_admin_editing_missing_document_gets_not_found(client, login_as):
    headers = login_as("admin@atlas.test", "AtlasAdmin123!")

    response = client.patch("/api/docs/999999", headers=headers, json={"title": "Missing"})

    assert response.status_code == 404
