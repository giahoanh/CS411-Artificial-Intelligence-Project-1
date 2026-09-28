import os
import json
from pathlib import Path

from flask import Flask, render_template, jsonify, request
from uninformed import bfs, dfs, ucs, ids
from informed import greedy_best_first, a_star

app = Flask(__name__)

PROJECT_FOLDER = Path(__file__).resolve().parent
MAP_DATA_FILE = PROJECT_FOLDER / "map_data.json"


def load_map_data():
    """Load the saved Chicago graph from beside this file."""
    with open(MAP_DATA_FILE, "r") as file:
        data = json.load(file)
    return data


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/map", methods=["GET"])
def get_map():
    data = load_map_data()
    return jsonify(data)


@app.route("/api/search", methods=["POST"])
def search():
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({"error": "Send a JSON object."}), 400

    start = payload.get("start")
    goal = payload.get("goal")
    algorithm = payload.get("algorithm")

    for value in [start, goal, algorithm]:
        if not isinstance(value, str):
            return jsonify({"error": "Start, goal, and algorithm must be text."}), 400

    algorithms = {
        "bfs": bfs,
        "dfs": dfs,
        "ucs": ucs,
        "ids": ids,
        "greedy": greedy_best_first,
        "astar": a_star,
    }

    if algorithm not in algorithms:
        return jsonify({"error": "Unknown algorithm."}), 400

    data = load_map_data()
    cities = data["nodes"]

    if start not in cities or goal not in cities:
        return jsonify({"error": "Unknown source or destination."}), 400

    search_function = algorithms[algorithm]
    result = search_function(data, start, goal)
    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)
