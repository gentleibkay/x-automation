from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from storage import list_drafts, approve_draft, init_db

app = Flask(__name__)

# Make sure templates auto-refresh
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure DB is created when web server starts
@app.before_first_request
def setup_database():
    print("Initializing database...")
    init_db()


# -----------------------
# HOME PAGE — SHOW DRAFTS
# -----------------------
@app.route("/")
def index():
    try:
        drafts = list_drafts()
        print("Loaded drafts:", drafts)
    except Exception as e:
        print("Error loading drafts:", e)
        drafts = []

    return render_template("index.html", drafts=drafts)


# -----------------------
# APPROVE & PUBLISH BUTTON
# -----------------------
@app.route("/approve/<int:draft_id>", methods=["POST"])
def approve(draft_id):
    print(f"Approving draft {draft_id}")
    try:
        approve_draft(draft_id)
    except Exception as e:
        print("Error approving draft:", e)

    return redirect(url_for("index"))


# -----------------------
# SERVE GENERATED IMAGE FILES
# -----------------------
@app.route("/generated/<path:filename>")
def serve_generated(filename):
    """
    Your worker saves images into generated/ folder.
    This route makes them accessible as /generated/<file>
    """
    directory = os.path.join(os.getcwd(), "generated")
    return send_from_directory(directory, filename)


# -----------------------
# MAIN ENTRY
# -----------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
