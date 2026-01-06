from flask import Flask, render_template, request
from app.ai_engine import generate_ai_response
from flask import jsonify
from app.db import init_db, get_db
from flask import session
import uuid
init_db()
app = Flask(__name__)


app.secret_key = "a/slknflksdgndslkgndsok'lgn dsl,gndslkgnldskgndslkgn"  # change in production

@app.before_request
def assign_user():
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", response="")

@app.route("/ask", methods=["POST"])
def ask():
    query = request.form.get("query", "")
    response = generate_ai_response(query)
    return render_template("index.html", response=response)

@app.route("/online-python")
def online_python():
    return render_template("online_python.html")


@app.route("/save-snippet", methods=["POST"])
def save_snippet():
    code = request.json.get("code")
    user_id = session["user_id"]

    db = get_db()
    db.execute(
        "INSERT INTO snippets (user_id, code) VALUES (?, ?)",
        (user_id, code)
    )
    db.commit()
    db.close()

    return jsonify({"status": "saved"})

@app.route("/snippets")
def snippets():
    db = get_db()
    rows = db.execute("SELECT id, code, created_at FROM snippets").fetchall()
    db.close()
    return render_template("snippets.html", snippets=rows)

@app.route("/load-snippets")
def load_snippets():
    user_id = session["user_id"]
    db = get_db()
    rows = db.execute(
        "SELECT id, code, created_at FROM snippets WHERE user_id=? ORDER BY id DESC",
        (user_id,)
    ).fetchall()
    db.close()

    return jsonify([
        {"id": r[0], "code": r[1], "created_at": r[2]}
        for r in rows
    ])


@app.route("/save-draft", methods=["POST"])
def save_draft():
    code = request.json.get("code")
    user_id = session["user_id"]

    db = get_db()
    db.execute(
        "INSERT OR REPLACE INTO drafts (user_id, code) VALUES (?, ?)",
        (user_id, code)
    )
    db.commit()
    db.close()
    return jsonify({"status": "draft saved"})

@app.route("/load-draft")
def load_draft():
    user_id = session["user_id"]
    db = get_db()
    row = db.execute(
        "SELECT code FROM drafts WHERE user_id=?",
        (user_id,)
    ).fetchone()
    db.close()

    return jsonify({"code": row[0] if row else ""})

# ---------------- DELETE ONE SNIPPET ----------------
@app.route("/delete-snippet/<int:snippet_id>", methods=["DELETE"])
def delete_snippet(snippet_id):
    user_id = session["user_id"]
    db = get_db()
    db.execute(
        "DELETE FROM snippets WHERE id=? AND user_id=?",
        (snippet_id, user_id)
    )
    db.commit()
    db.close()
    return jsonify({"status": "deleted"})


# ---------------- DELETE ALL SNIPPETS ----------------
@app.route("/delete-all-snippets", methods=["DELETE"])
def delete_all_snippets():
    user_id = session["user_id"]
    db = get_db()
    db.execute(
        "DELETE FROM snippets WHERE user_id=?",
        (user_id,)
    )
    db.commit()
    db.close()
    return jsonify({"status": "all deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
