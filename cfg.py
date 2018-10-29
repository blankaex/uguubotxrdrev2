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
