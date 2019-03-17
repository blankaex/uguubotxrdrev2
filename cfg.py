import socket
import re

HOST = "irc.twitch.tv"
PORT = 6667
NICK = "UguuBotXrdRev2"
PASS = # Redacted
ACPT = "application/vnd.twitchtv.v5+json"
CLID = # Redacted
AUTH = # Redacted
CURL = "https://api.twitch.tv/kraken/channels/41790391"
CHAN = "#blankaexx"
RATE = (20/30)
CHAT = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
MODS = ["blankaexx"]
CMDL = ["time", "link", "twitter", "youtube", "paizuri"]

def isCommand(line):
    return line[0] == '!'

def getName(line):
    return re.search(r"\w+", line).group(0)

def getMsg(line):
    return CHAT.sub("", line).strip()

def chat(sock, msg):
    sock.send(("PRIVMSG {} :{}\r\n".format(CHAN, msg)).encode("utf-8"))
