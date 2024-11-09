import requests
import json
import os
# Set variables
ENDPOINT = "https://nova-litellm-proxy.onrender.com"
MASTER_KEY = os.getenv("MASTER_KEY")
TEAM_NAMES = ["TeamA", "TeamB", "TeamC"]  # Replace with your actual team names
MAX_BUDGET_FLOAT = 10.0  # Example budget value

# Define headers
headers = {
    "Authorization": f"Bearer {MASTER_KEY}",
    "Content-Type": "application/json"
}

# Dictionary to store team name to generated key mapping
team_key_mapping = {}

for team_name in TEAM_NAMES:
    # First request: create a new team
    create_team_data = {
        "team_alias": team_name,
        "max_budget": MAX_BUDGET_FLOAT
    }

    try:
        response = requests.post(f"{ENDPOINT}/team/new", headers=headers, json=create_team_data)
        response.raise_for_status()  # Raise an error for bad status codes
        team_id = response.json().get("team_id")
        if not team_id:
            raise ValueError(f"Failed to retrieve team_id for team {team_name}")
        print(f"Created team {team_name} with ID: {team_id}")

    except requests.exceptions.RequestException as e:
        print(f"Error creating team {team_name}: {e}")
        continue
    except ValueError as e:
        print(e)
        continue

    # Second request: generate a key for the created team
    generate_key_data = {
        "team_id": team_id
    }

    try:
        key_response = requests.post(f"{ENDPOINT}/key/generate", headers=headers, json=generate_key_data)
        key_response.raise_for_status()
        generated_key = key_response.json().get("key")
        if not generated_key:
            raise ValueError(f"Failed to retrieve key for team {team_name}")
        print(f"Generated Key for team {team_name}: {generated_key}")

        # Add to mapping
        team_key_mapping[team_name] = generated_key

    except requests.exceptions.RequestException as e:
        print(f"Error generating key for team {team_name}: {e}")
    except ValueError as e:
        print(e)

# Output the mapping of team names to API keys
print("\nTeam to API Key Mapping:")
for team, api_key in team_key_mapping.items():
    print(f"{team}: {api_key}")