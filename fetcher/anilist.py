import requests

API_URL = "https://graphql.anilist.co"

QUERY = """
query ($id: Int) {
  Media (id: $id, type: ANIME) {
    id
    title { romaji }
    description
    coverImage { large }
    startDate { year }
  }
}
"""

def fetch_anime(anime_id):
    r = requests.post(API_URL, json={
        "query": QUERY,
        "variables": {"id": anime_id}
    })
    if r.status_code != 200:
        return None
    return r.json().get("data", {}).get("Media")
