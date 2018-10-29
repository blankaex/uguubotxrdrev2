import socket
import time
import re
from cfg import *
from cmd import *

s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))

while True:
    line = s.recv(1024).decode("utf-8")
    if line == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        name = re.search(r"\w+", line).group(0)
        msg = CHAT.sub("", line).strip()
        print("{}: {}".format(name, msg))
        if msg[0] == '!': # tried to do backwards if and failed
            handle(s, name, msg[1:]) 
    time.sleep(RATE) # should be 1/rate but I get div by 0??
