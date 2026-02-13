from flask import Flask
from polycule import Polycules

app = Flask(__name__)

polycules = Polycules()

@app.route("/polycule/<guid>")
def view_graph(guid):
    return polycules.get(guid).render_graph_to_html()

def migrate():
    pass