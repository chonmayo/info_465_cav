import requests
import config

def craft_request():
    url = "https://www.arcgis.com/sharing/rest/oauth2/token"

    payload = {'client_id': config.client_id,
    'client_secret': config.client_secret,
    'grant_type': 'client_credentials'}
    files = [

    ]
    headers= {}

    response = requests.request("POST", url, headers=headers, data = payload, files = files)

    print(response.text)

craft_request()