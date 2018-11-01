import socket
import re

HOST = "irc.twitch.tv"
PORT = 6667
NICK = "UguuBotXrdRev2"
PASS = # Redacted
CHAN = "#blankaexx"
RATE = (20/30)
CHAT = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
MODS = ["blankaexx"]

def isCommand(line):
    return line[0] == '!'

def getName(line):
    return re.search(r"\w+", line).group(0)

def getMsg(line):
    return CHAT.sub("", line).strip()

def chat(sock, msg):
    sock.send(("PRIVMSG {} :{}\r\n".format(CHAN, msg)).encode("utf-8"))
