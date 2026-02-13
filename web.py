from flask import Flask
from polycule import Polycule

app = Flask(__name__)

@app.route("/polycule/<guid>")
def view_graph(guid):
    return Polycule(guid).render_graph_to_html()

def migrate():
    pass