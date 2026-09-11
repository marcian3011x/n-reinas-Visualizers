from flask import Flask, request, jsonify, render_template
from genetic_algorithm import genetic_algorithm

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json()

    n = data.get("n", 8)
    population_size = data.get("population_size", 100)
    generations = data.get("generations", 500)
    mutation_rate = data.get("mutation_rate", 0.2)

    solution, fitness_history, boards_history, gens_used, found = genetic_algorithm(
        n, population_size, generations, mutation_rate
    )

    return jsonify({
        "found": found,
        "solution": solution.tolist() if solution is not None else None,
        "fitness_history": [int(v) for v in fitness_history],
        "boards_history": boards_history,
        "generations_used": gens_used,
    })

if __name__ == "__main__":
    app.run(debug=True)