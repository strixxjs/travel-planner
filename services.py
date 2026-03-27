import requests

def get_place_from_api(external_id: str):
    url = f"https://api.artic.edu/api/v1/artworks/{external_id}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "exists": True,
            "title": data["data"]["title"]
        }
    return {"exists": False, "title": None}