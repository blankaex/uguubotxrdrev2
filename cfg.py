import re
import requests
import socket
import time

HOST = "irc.twitch.tv"
PORT = 6667
NICK = "UguuBotXrdRev2"
PASS = # Redacted
CHAN = "#blankaexx"
RATE = (20/30)
CHAT = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
MODS = ["blankaexx"]

MOD_COMMANDS = {
    "ban"       : ["ban", "b", "kb"],
    "unban"     : ["unban", "ub", "free"],
    "timeout"   : ["timeout", "to", "time"],
    "title"     : ["title"],
    "game"      : ["game", "category"],
}

COMMANDS = {
    "help"      : ["commands", "list", "help"],
    "time"      : ["time", "t", "currtime", "ct"],
    "uptime"    : ["uptime", "ut"],
    "link"      : ["link", "stream", "streamlink", "twitch"],
    "twitter"   : ["twitter", "tweet"],
    "youtube"   : ["youtube", "yt"]
}
