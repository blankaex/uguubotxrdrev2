import requests
import socket
import json
import re

f = open("auth.json", "r")
tokens = dict(json.loads(f.read()))
f.close()

HOST = "irc.twitch.tv"
PORT = 6667
CHAN = "#blankaexx"
NICK = "UguuBotXrdRev2"
PASS = tokens["password"]
CLID = tokens["client-id"]
CLSC = tokens["client-secret"]
AUTH = tokens["access-token"]
RFTO = tokens["refresh-token"]
ACPT = "application/vnd.twitchtv.v5+json"
CURL = "https://api.twitch.tv/kraken/channels/41790391"
RATE = (20/30)
CHAT = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
MODS = ["blankaexx"]
CMDL = ["time", "link", "twitter", "tweet", "youtube", "paizuri"]
TWCH = "https://www.twitch.tv/blankaexx"
TWIT = "https://twitter.com/blankaex"
YOUT = "https://www.youtube.com/blankaex"

def isCommand(line):
    return line[0] == '!'

def getName(line):
    return re.search(r"\w+", line).group(0)

def getMsg(line):
    return CHAT.sub("", line).strip()

def chat(sock, msg):
    sock.send(("PRIVMSG {} :{}\r\n".format(CHAN, msg)).encode("utf-8"))

def refreshToken():
    global CLID, CLSC, AUTH, RFTO
    params = {'grant_type': 'refresh_token', 'refresh_token': RFTO, 'client_id': CLID, 'client_secret': CLSC}
    r = requests.post('https://id.twitch.tv/oauth2/token', params=params)
    response = dict(r.json())
    tokens["access-token"] = "OAuth " + response["access_token"]
    AUTH = tokens["access-token"]
    tokens["refresh-token"] = response["refresh_token"]
    RFTO = tokens["refresh-token"]
    f = open("auth.json", "w")
    f.write(json.dumps(tokens))
    f.close()
