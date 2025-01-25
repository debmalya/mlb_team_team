from flask import Flask, jsonify, request, render_template
# general data science library
import pandas as pd
import numpy as np

# pulling data from APIs, parsing JSON
import requests
import json


# interfacing w/ Cloud storage from python
from google.cloud import storage

# Plotting
import matplotlib.pyplot as plt
import seaborn as sns


app = Flask(__name__)

# Sample MLB data (replace with actual data from the hackathon)
mlb_data = {
    "teams": [
        {"name": "Arizona Diamondbacks", "id": 109},
        {"name": "Atlanta Braves", "id": 144},
        {"name": "Baltimore Orioles", "id": 110},
        {"name": "Boston Red Sox", "id": 111},
        {"name": "Chicago White Sox", "id": 145},
        {"name": "Chicago Cubs", "id": 112},
        {"name": "Cincinnati Reds", "id": 113},
        {"name": "Cleveland Guardians", "id": 114},
        {"name": "Colorado Rockies", "id": 115},
        {"name": "Detroit Tigers", "id": 116},
        {"name": "Houston Astros", "id": 117},
        {"name": "Kansas City Royals", "id": 118},
        {"name": "Los Angeles Angels", "id": 108},
        {"name": "Los Angeles Dodgers", "id": 119},
        {"name": "Miami Marlins", "id": 146},
        {"name": "Milwaukee Brewers", "id": 158},
        {"name": "Minnesota Twins", "id": 142},
        {"name": "New York Yankees", "id": 147},
        {"name": "New York Mets", "id": 121},
        {"name": "Oakland Athletics", "id": 133},
        {"name": "Philadelphia Phillies", "id": 143},
        {"name": "Pittsburgh Pirates", "id": 134},
        {"name": "San Diego Padres", "id": 135},
        {"name": "San Francisco Giants", "id": 137},
        {"name": "Seattle Mariners", "id": 136},
        {"name": "St. Louis Cardinals", "id": 138},
        {"name": "Tampa Bay Rays", "id": 139},
        {"name": "Texas Rangers", "id": 140},
        {"name": "Toronto Blue Jays", "id": 141},
        {"name": "Washington Nationals", "id": 120}
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
    if request.method == "POST":
        team1 = request.form.get("team1")
        team2 = request.form.get("team2")
        team1_name = next((team["name"] for team in mlb_data["teams"] if team["id"] == int(team1)), None)
        team2_name = next((team["name"] for team in mlb_data["teams"] if team["id"] == int(team2)), None)
        # Perform comparison logic here (example below)
        comparison_result = f"Comparing {team1_name} vs {team2_name}" 
        return render_template("comparison.html", result=comparison_result, teams=mlb_data["teams"]) # Pass teams to template
    return render_template("comparison.html", teams=mlb_data["teams"]) # Pass teams to template

if __name__ == "__main__":
    app.run(debug=True)
