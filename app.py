import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from storage import list_drafts, approve_draft, publish_draft, init_db

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "changeme")

# -------------------------
# Create database on startup
# -------------------------
with app.app_context():
    try:
        init_db()
        print("Database initialized.")
    except Exception as e:
        print("Error initializing DB:", e)


# -------------------------
# Serve static files
# -------------------------
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


# -------------------------
# Admin UI
# -------------------------
@app.route("/")
def index():
    drafts = list_drafts()
    return render_template("index.html", drafts=drafts)


# -------------------------
# Approve + Publish
# -------------------------
@app.route("/approve/<int:draft_id>", methods=["POST"])
def approve(draft_id):
    approve_draft(draft_id)
    publish_draft(draft_id)
    return redirect(url_for("index"))


# -------------------------
# Run server
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
