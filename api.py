import json
import requests


def refresh_tokens(bot):
    URL = 'https://id.twitch.tv/oauth2/token'
    params = {
        'grant_type': 'refresh_token', 
        'refresh_token': bot.refresh_token,
        'client_id': bot.client_id,
        'client_secret': bot.client_secret
    }

    response = requests.post(URL, params=params)

    if not response.status_code == requests.codes.ok:
        raise Exception(f"{response.status_code} response.")

    response = response.json()

    bot.access_token = "OAuth " + response["access_token"]
    bot.refresh_token = response["refresh_token"]

    with open("auth.json", "r") as f:
        tokens = json.load(f)
        tokens["access-token"] = bot.access_token
        tokens["refresh-token"] = bot.refresh_token

    with open("auth.json", "w") as f:
        json.dump(tokens, f, sort_keys=True, indent=4, separators=(',', ': '))
        f.truncate()


def get_channel(bot):
    URL = f"https://api.twitch.tv/v5/channels/{bot.channel_id}"
    headers = {
        "Accept": "application/vnd.twitchtv.v5+json",
        "Client-ID": bot.client_id
    }
    response = requests.get(URL, headers=headers)
    if response.status_code == requests.codes.ok:
        return json.loads(response.text)
    else:
        raise Exception(f"{response.status_code} response.")


def update_channel(bot, data):
    refresh_tokens(bot)
    URL = f"https://api.twitch.tv/v5/channels/{bot.channel_id}"
    headers = {
        "Accept": "application/vnd.twitchtv.v5+json",
        "Client-ID": bot.client_id,
        "Authorization": bot.access_token
    }
    response = requests.put(URL, headers=headers, data=data)
    if response.status_code == requests.codes.ok:
        return json.loads(response.text)
    else:
        raise Exception(f"{response.status_code} response.")


def shorten_url(bot, link):
    URL = "https://0x0.st"
    data = { "shorten": link }
    response = requests.post(URL, data=data)
    if response.status_code == requests.codes.ok:
        return response.text
    else:
        raise Exception(f"{response.status_code} response.")
