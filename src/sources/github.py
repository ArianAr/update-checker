import requests
import json


def fetch_from_github(program):
    github_url = f"https://api.github.com/repos/{program['github']}/releases/latest"
    response = requests.get(github_url)
    response.raise_for_status()
    github_data = response.json()
    return github_data