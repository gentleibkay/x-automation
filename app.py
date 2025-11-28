import os
from flask import Flask, render_template, request, redirect
from storage import list_drafts, delete_draft

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route("/")
def index():
    drafts = list_drafts()
    return render_template("index.html", drafts=drafts)


@app.route("/approve/<int:draft_id>", methods=["POST"])
def approve(draft_id):
    # TODO: add X publishing later
    delete_draft(draft_id)
    return redirect("/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
