from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token

def get_auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }

# get each track from playlist
def get_tracks_from_playlist(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_headers(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]

    array_return = []

    for result in json_result:
        array_return.append(result["track"]["name"])
    
    return array_return

# search for tracks that are contained in 2 playlists
def get_tracks_in_two_playlists(token, playlist1, playlist2):
    array1 = get_tracks_from_playlist(token, playlist1)
    array2 = get_tracks_from_playlist(token, playlist2)

    return find_common_elements(array1, array2)

def find_common_elements(arr1, arr2):
    common_elements = []

    for element in arr1:
        if element in arr2:
            common_elements.append(element)

    return common_elements
    

token = get_token()
final_array = get_tracks_in_two_playlists(token, "3N2LBm2643sqjxXAdZYqOE", "2v5dKrptkVKLI9yUAuB8KO")

for track in final_array:
    print(track)