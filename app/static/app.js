let token = null;
let currentUser = null;
let selectedDoc = null;
let currentDoc = null;
let documentRequest = 0;
let searchRequest = 0;
let searchActive = false;
let searchQuery = "";
let saving = false;
const $ = (id) => document.getElementById(id);
const orgName = (id) => ({ 1: "Atlas", 2: "Boreal" }[id] || `Organization ${id}`);

async function api(path, options = {}) {
  const res = await fetch(path, {
    ...options,
    headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}), ...(options.headers || {}) }
  });
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
  return await res.json();
}
function errorMessage(e) { $("error").textContent = e.message || String(e); $("error").hidden = false; }
function clearError() {
  $("error").textContent = ""; $("error").hidden = true;
  $("status").textContent = ""; $("status").hidden = true;
}
function statusMessage(message) { $("status").textContent = message; $("status").hidden = false; }
function markSelection() {
  document.querySelectorAll(".doc-button").forEach(button => {
    button.setAttribute("aria-current", String(Number(button.dataset.docId) === selectedDoc));
    button.disabled = saving;
  });
}
function itemList(el, docs) {
  el.replaceChildren();
  for (const d of docs) {
    const li = document.createElement("li");
    const btn = document.createElement("button");
    btn.type = "button"; btn.className = "doc-button"; btn.dataset.docId = d.id;
    const icon = document.createElement("span");
    icon.className = "doc-icon"; icon.textContent = "▤"; icon.setAttribute("aria-hidden", "true");
    const copy = document.createElement("span"); copy.className = "doc-copy";
    const title = document.createElement("span"); title.className = "doc-name"; title.textContent = d.title;
    const meta = document.createElement("span"); meta.className = "doc-id"; meta.textContent = `Document #${d.id}`;
    copy.append(title, meta); btn.append(icon, copy);
    btn.onclick = () => showDoc(d.id).catch(errorMessage);
    li.append(btn); el.append(li);
  }
  if (!docs.length) {
    const li = document.createElement("li"); li.className = "list-empty";
    li.textContent = el.id === "results" ? "No documents match your search." : "No documents yet.";
    el.append(li);
  }
  markSelection();
}
async function refreshDocs() {
  const docs = await api("/api/docs");
  itemList($("docs"), docs); $("doc-count").textContent = docs.length;
  return docs;
}
function closeEditor() {
  $("edit-form").hidden = true;
  $("document-view").hidden = false;
  $("edit-doc").hidden = !currentDoc || currentUser?.role !== "admin";
}
function renderDoc(doc) {
  currentDoc = doc; selectedDoc = doc.id;
  $("doc-title").textContent = doc.title;
  $("doc-content").textContent = doc.content;
  $("doc-meta").textContent = `${orgName(doc.org_id)} / Document #${doc.id}`;
  $("empty-state").hidden = true; $("document-panel").hidden = false;
  $("comment-form").hidden = false;
  closeEditor(); markSelection();
}
async function showDoc(docId) {
  if (saving) return;
  clearError();
  const request = ++documentRequest;
  const doc = await api(`/api/docs/${docId}`);
  if (request !== documentRequest) return;
  renderDoc(doc);
  $("comments").replaceChildren(); $("comment-count").textContent = "…";
  $("comment-text").value = "";
  await refreshComments();
}
async function refreshComments() {
  const docId = selectedDoc;
  const request = documentRequest;
  const comments = await api(`/api/docs/${docId}/comments`);
  if (docId !== selectedDoc || request !== documentRequest) return;
  $("comment-count").textContent = comments.length;
  const el = $("comments");
  // Deliberately imperfect rendering in this training snapshot; review in the AppSec phase.
  el.innerHTML = comments.map(c => `<p><strong>${c.author}</strong>${c.body}</p>`).join("") || '<p class="comments-empty">No comments yet. Start the conversation.</p>';
}
function resetWorkspace() {
  token = null; currentUser = null; selectedDoc = null; currentDoc = null;
  ++documentRequest; ++searchRequest;
  searchActive = false; searchQuery = "";
  $("app-panel").hidden = true; $("login-panel").hidden = false;
  $("document-panel").hidden = true; $("empty-state").hidden = false;
  $("edit-form").reset(); closeEditor();
  $("search-form").reset(); $("comment-form").reset();
  $("search-results").hidden = true; $("docs").hidden = false;
  $("comments").replaceChildren(); $("docs").replaceChildren(); $("results").replaceChildren();
  clearError();
}
$("login-form").onsubmit = async (e) => {
  e.preventDefault(); clearError();
  $("login-submit").disabled = true;
  try {
    const auth = await api("/api/auth/login", { method: "POST", body: JSON.stringify({email: $("email").value, password: $("password").value}) });
    token = auth.access_token;
    currentUser = await api("/api/me");
    $("who").textContent = currentUser.email;
    $("role").textContent = currentUser.role;
    $("user-avatar").textContent = currentUser.email.slice(0, 2).toUpperCase();
    $("workspace-title").textContent = `${orgName(currentUser.org_id)} workspace`;
    const docs = await refreshDocs();
    $("login-panel").hidden = true; $("app-panel").hidden = false;
    if (docs.length) await showDoc(docs[0].id);
  } catch (e) {
    if ($("app-panel").hidden) resetWorkspace();
    errorMessage(e);
  } finally { $("login-submit").disabled = false; }
};
async function runSearch() {
  const request = ++searchRequest;
  const docs = await api(`/api/docs/search?q=${encodeURIComponent(searchQuery)}`);
  if (request !== searchRequest || !searchActive) return;
  itemList($("results"), docs);
  $("search-results").hidden = false; $("docs").hidden = true;
}
$("search-form").onsubmit = async (e) => {
  e.preventDefault(); clearError();
  searchQuery = $("search").value; searchActive = true;
  try { await runSearch(); } catch (err) { errorMessage(err); }
};
$("clear-search").onclick = () => {
  ++searchRequest; searchActive = false; searchQuery = "";
  $("search").value = ""; $("search-results").hidden = true; $("docs").hidden = false;
  clearError();
};
$("edit-doc").onclick = () => {
  if (currentUser?.role !== "admin" || !currentDoc) return;
  clearError();
  $("edit-title").value = currentDoc.title; $("edit-content").value = currentDoc.content;
  $("document-view").hidden = true; $("edit-doc").hidden = true; $("edit-form").hidden = false;
  $("edit-title").focus();
};
$("cancel-edit").onclick = () => { clearError(); closeEditor(); $("edit-doc").focus(); };
$("edit-form").onsubmit = async (e) => {
  e.preventDefault(); clearError();
  if (saving || currentUser?.role !== "admin" || !currentDoc) return;
  const title = $("edit-title").value.trim();
  if (!title) { errorMessage(new Error("Please enter a document title.")); $("edit-title").focus(); return; }
  ++documentRequest;
  saving = true;
  ["save-doc", "cancel-edit", "logout", "edit-title", "edit-content", "edit-doc"].forEach(id => { $(id).disabled = true; });
  $("save-doc").textContent = "Saving…"; markSelection();
  try {
    const doc = await api(`/api/docs/${selectedDoc}`, { method: "PATCH", body: JSON.stringify({ title, content: $("edit-content").value }) });
    renderDoc(doc); statusMessage("Changes saved.");
    try { await refreshDocs(); if (searchActive) await runSearch(); }
    catch (err) { errorMessage(new Error(`Your document was saved, but the list could not be refreshed. ${err.message}`)); }
  } catch (err) { errorMessage(err); }
  finally {
    saving = false;
    ["save-doc", "cancel-edit", "logout", "edit-title", "edit-content", "edit-doc"].forEach(id => { $(id).disabled = false; });
    $("save-doc").textContent = "Save changes"; markSelection();
    if ($("edit-form").hidden) $("edit-doc").focus();
  }
};
$("comment-form").onsubmit = async (e) => {
  e.preventDefault(); clearError();
  const docId = selectedDoc;
  const request = documentRequest;
  const body = $("comment-text").value;
  $("post-comment").disabled = true;
  try {
    await api(`/api/docs/${docId}/comments`, {method:"POST", body:JSON.stringify({body})});
    if (docId !== selectedDoc || request !== documentRequest) return;
    $("comment-text").value = ""; await refreshComments();
  } catch (err) { errorMessage(err); }
  finally { $("post-comment").disabled = false; }
};
$("logout").onclick = resetWorkspace;
