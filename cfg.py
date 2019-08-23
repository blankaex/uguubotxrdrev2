import requests
import socket
import json
import re

HOST = "irc.twitch.tv"
PORT = 6667
CHAN = "#blankaexx"
NICK = "UguuBotXrdRev2"
ACPT = "application/vnd.twitchtv.v5+json"
CURL = "https://api.twitch.tv/kraken/channels/41790391"
RATE = (20/30)
CHAT = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
MODS = ["blankaexx"]
CMDL = ["help", "donate", "time", "link", "twitter", "tweet", "youtube", "paizuri"]
DNTE = "https://streamlabs.com/blankaexx"
TWCH = "https://www.twitch.tv/blankaexx"
TWIT = "https://twitter.com/blankaex"
YOUT = "https://www.youtube.com/blankaex"

def isCommand(line):
    return line[0] == '!'

def chat(sock, msg):
    sock.send(("PRIVMSG {} :{}\r\n".format(CHAN, msg)).encode("utf-8"))

def getName(line):
    return re.search(r"\w+", line).group(0)

def getMsg(line):
    return CHAT.sub("", line).strip()

def getAuth(key):
    with open("auth.json", "r") as f:
        return dict(json.load(f))[key]

def refreshToken():
    params = {
        'grant_type': 'refresh_token', 
        'refresh_token': getAuth('refresh-token'),
        'client_id': getAuth('client-id'),
        'client_secret': getAuth('client-secret')
    }
    r = requests.post('https://id.twitch.tv/oauth2/token', params=params)
    response = dict(r.json())

    # Write new token back to disk
    with open("auth.json", "r") as f:
        tokens = json.load(f)
        tokens["access-token"] = "OAuth " + response["access_token"]
        tokens["refresh-token"] = response["refresh_token"]

    with open("auth.json", "w") as f:
        json.dump(tokens, f, sort_keys=True, indent=4, separators=(',', ': '))
        f.truncate()
