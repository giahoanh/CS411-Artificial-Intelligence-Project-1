import json
from pathlib import Path

from flask import Flask, jsonify, request, render_template

from uninformed import bfs, dfs, ucs, ids
from informed import greedy_best_first, a_star


app = Flask(__name__)


current_file = Path(__file__).resolve()
project_folder = current_file.parent
map_file = project_folder / "map_data.json"

with open(map_file, "r") as graph_file:
    graph = json.load(graph_file)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/map")
def get_map():
    return jsonify(graph)


@app.route("/api/search", methods=["POST"])
def search():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        error_response = {
            "error": "Send a JSON object."
        }

        return jsonify(error_response), 400

    start = data.get("start")
    goal = data.get("goal")
    algorithm = data.get("algorithm")

    if not isinstance(start, str):
        error_response = {
            "error": "Start, goal, and algorithm must be text."
        }

        return jsonify(error_response), 400

    if not isinstance(goal, str):
        error_response = {
            "error": "Start, goal, and algorithm must be text."
        }

        return jsonify(error_response), 400

    if not isinstance(algorithm, str):
        error_response = {
            "error": "Start, goal, and algorithm must be text."
        }

        return jsonify(error_response), 400

    algorithms = {
        "bfs": bfs,
        "dfs": dfs,
        "ucs": ucs,
        "ids": ids,
        "greedy": greedy_best_first,
        "astar": a_star,
    }

    if algorithm not in algorithms:
        error_response = {
            "error": "Unknown algorithm."
        }

        return jsonify(error_response), 400

    cities = graph["nodes"]

    if start not in cities:
        error_response = {
            "error": "Unknown source or destination."
        }

        return jsonify(error_response), 400

    if goal not in cities:
        error_response = {
            "error": "Unknown source or destination."
        }

        return jsonify(error_response), 400

    search_function = algorithms[algorithm]

    search_result = search_function(graph, start, goal)
    return jsonify(search_result)

if __name__ == "__main__":
    app.run(port=5001)