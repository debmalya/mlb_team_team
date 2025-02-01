import os
from flask import Flask, jsonify, request, render_template


# pulling data from APIs, parsing JSON
import requests
import json
import pandas as pd
import datetime




print("Before app creation")
app = Flask(__name__)
app.config['THREADED'] = False
print("After app creation")
# Import routes *after* creating the app instance
# from app import routes  # Move this *after* the current_season assignment

# Function to get the current MLB season
def get_current_mlb_season():
    now = datetime.datetime.now()
    current_year = now.year
    # Adjust this logic based on when the MLB season typically starts and ends.
    # For example, if the season typically starts in April, you might use:
    if now.month < 4:  # Before April, use the previous year
        current_season = current_year - 1
    else:
        current_season = current_year
    return current_season

# 1. Call get_current_mlb_season() to get current_season
current_season = get_current_mlb_season()




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


#@title Function to Load Newline Delimited JSON into Pandas DF
def load_newline_delimited_json(url):
    """Loads a newline-delimited JSON file from a URL into a pandas DataFrame.

    Args:
        url: The URL of the newline-delimited JSON file.

    Returns:
        A pandas DataFrame containing the data, or None if an error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        data = []
        for line in response.text.strip().split('\n'):
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Skipping invalid JSON line: {line} due to error: {e}")

        return pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading data: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    

 

@app.route("/api/teams")
def get_teams():
    return jsonify(mlb_data["teams"])

@app.route("/api/players")
def get_players():
    return jsonify(mlb_data["players"])

def get_team_stats(team_id, season):
    url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/stats?season={season}" # Example using team endpoint
    response = requests.get(url)

    if response.status_code == 200:
        team_stats = response.json()
        # Extract specific stats like wins, losses, batting average, ERA, stolen bases, etc. from team_stats
        return team_stats.get("stats", [{}])[0].get("splits", [{}])[0].get("stat")  #Navigate JSON to the stats

    else:
        print(f"Error: {response.status_code}")  # Handle API errors
        return None
    

def get_current_season_from_standings():
    url = "https://statsapi.mlb.com/api/v1/standings" # No season parameter, will give current standings.
    response = requests.get(url)

    if response.status_code == 200:
        standings_data = response.json()
        print(standings_data)
        # The season is part of the records returned in the standings data
        # You'll need to examine the response structure to extract it correctly
        return standings_data['records'][0]['season'] # Extract season from first record.
    else:
        # Handle errors
        print(f"Error getting current MLB season from standings: {response.status_code}")
        return None
   


def get_current_mlb_season():
    url = "https://statsapi.mlb.com/api/v1/sports"
    response = requests.get(url)

    if response.status_code == 200:
        sports_data = response.json()
        for sport in sports_data['sports']:
            if sport['id'] == 1:  # MLB's sportId is 1
                return sport['currentSeason']  # Extract currentSeason
    else:
        # Handle errors (e.g., log the error, return a default value)
        print(f"Error getting current MLB Season: {response.status_code}")
        return None
    
@app.route("/api/team_performance")
def get_team_performance():
    df = fetch_mlb_team_performance_data()
    if df is not None:
        return jsonify(df.to_dict(orient="records"))
    return jsonify({"error": "Failed to fetch data"}), 500

@app.route("/api/team_stats/<int:season>")
def fetch_mlb_team_performance_data(season):
    url = "https://statsapi.mlb.com/api/v1/teams/stats"
    params = {
        "season": season,
        "sportId": "1",
        "group": "hitting,pitching,fielding",
        "stats": "season"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        teams_stats = data.get("stats", [])
        print(teams_stats)
        # return pd.DataFrame(teams_stats)
        return teams_stats
    except requests.exceptions.RequestException as e:
        print(f"Error downloading data: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Function to get team stats from JSON file
def get_team_stats_from_json(team_id,season):
    try:
        with open(f'data/{season}.json', 'r') as file:
            data = json.load(file)
            team_stats = {}
            for group in data:
            
                group_name =group["group"]["displayName"]
            
                for splits in group.get("splits"):
                
                    if splits["team"]["id"] == int(team_id):
                        # team_stats['rank'] = splits["rank"]
                        team_stats[group_name] = splits["stat"]
                        break
            return team_stats
        
    except FileNotFoundError:
        print(f"File not found: data/{season}.json")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: data/{season}.json")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def compare_teams():
    if request.method == "POST":
        team1 = request.form.get("team1")
        team2 = request.form.get("team2")
        
        season1 = int(request.form.get("season1"))
        season2 = int(request.form.get("season2"))
        
        team1_name = next((team["name"] for team in mlb_data["teams"] if team["id"] == int(team1)), None)
        team2_name = next((team["name"] for team in mlb_data["teams"] if team["id"] == int(team2)), None)
        team1_logo = f'https://www.mlbstatic.com/team-logos/{team1}.svg'
        team2_logo = f'https://www.mlbstatic.com/team-logos/{team2}.svg'

        team1_stats = get_team_stats_from_json(team1, season1)
        team2_stats = get_team_stats_from_json(team2, season2)
       
        # Perform comparison logic here (example below)
        # comparison_result = f"Comparing {team1_name} vs {team2_name}" 
        if team1_stats is None or team2_stats is None:
            return render_template("comparison.html", error="Error fetching team stats", teams=mlb_data["teams"])
        comparison_result = f"{team1_name} Stats: {team1_stats}\n"
        comparison_result += f"{team2_name} Stats: {team2_stats}"
        return render_template("comparison.html", result=comparison_result, team1=team1_name, team2=team2_name, team1_logo=team1_logo, team2_logo=team2_logo, teams=mlb_data["teams"],team1_stats=team1_stats, team2_stats=team2_stats,season1=season1,season2=season2)
    return render_template("comparison.html", teams=mlb_data["teams"]) # Pass teams to template



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print("Before main block")
    app.run(host="0.0.0.0", port=port, debug=True) # or app.run(debug=True) if port can be auto-detected.
    


print("After main block")