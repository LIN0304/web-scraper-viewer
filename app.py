from flask import Flask, render_template, send_from_directory, abort
import os, markdown, json

APP_DIR  = os.path.dirname(__file__)
DATA_DIR = os.path.join(APP_DIR, "scraped_data")

app = Flask(__name__)

def list_pairs() -> list[tuple[str, str]]:
    """Returns sorted list of (md_file, json_file) pairs."""
    md_files = sorted(f for f in os.listdir(DATA_DIR) if f.endswith(".md"))
    pairs = []
    for md in md_files:
        stem = md[:-3]                     # e.g. page_0
        json_name = f"{stem}_original.json"
        pairs.append((md, json_name if os.path.exists(os.path.join(DATA_DIR, json_name)) else None))
    return pairs

@app.route("/")
def index():
    pairs = list_pairs()
    return render_template("index.html",
                           pairs=pairs,
                           count=len(pairs),
                           title="Scraped Articles")

@app.route("/view/<path:filename>")
def view_file(filename):
    if not filename.endswith(".md"):
        filename += ".md"
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        abort(404)
    with open(path, encoding="utf-8") as f:
        html = markdown.markdown(f.read(), extensions=["fenced_code", "tables"])
    return render_template("view.html",
                           content=html,
                           filename=filename,
                           count=len(list_pairs()),
                           title=filename)

@app.route("/raw/<path:filename>")
def raw_file(filename):
    return send_from_directory(DATA_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
