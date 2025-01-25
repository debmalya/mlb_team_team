
import requests
# from flask import Flask, jsonify, request, render_template

def get_mlb_team_ids():
    url = "https://statsapi.mlb.com/api/v1/teams?sportId=1"
    print("Fetching MLB team IDs...")
    response = requests.get(url)
    print(f"Response status code: {response.status_code}")
    if response.status_code == 200:
        teams = response.json().get('teams', [])
        team_ids = {team['name']: team['id'] for team in teams}
        print("Team IDs retrieved successfully.")
        print(team_ids)
        return team_ids
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return {}

if __name__ == "__main__":
    team_ids = get_mlb_team_ids()
    for team_name, team_id in team_ids.items():
        print(f"{team_name}: {team_id}")
