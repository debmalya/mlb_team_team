from flask import Flask, jsonify, request, render_template


app = Flask(__name__)

# Sample MLB data (replace with actual data from the hackathon)
mlb_data = {
    "teams": [
        {"name": "New York Yankees", "league": "AL"},
        {"name": "Los Angeles Dodgers", "league": "NL"},
        # ... more teams
    ],
    "players": [
        {"name": "Aaron Judge", "team": "New York Yankees", "position": "OF"},
        {"name": "Mookie Betts", "team": "Los Angeles Dodgers", "position": "OF"},
        # ... more players
    ]
}

@app.route("/api/teams")
def get_teams():
    return jsonify(mlb_data["teams"])

@app.route("/api/players")
def get_players():
    return jsonify(mlb_data["players"])


@app.route("/", methods=["GET", "POST"])
def compare_teams():
    if request.method == "GET":
        team1 = request.form.get("team1")
        team2 = request.form.get("team2")
        # Perform comparison logic here (example below)
        comparison_result = f"Comparing {team1} vs {team2}" 
        return render_template("comparison.html", result=comparison_result, teams=mlb_data["teams"]) # Pass teams to template
    return render_template("comparison.html", teams=mlb_data["teams"]) # Pass teams to template

if __name__ == "__main__":
    app.run(debug=True)
