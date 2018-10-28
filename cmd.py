import socket
from cfg import *

def chat(sock, msg):
    sock.send(("PRIVMSG {} :{}\r\n".format(CHAN, msg)).encode("utf-8"))

def ban(sock, user):
    chat(sock, ".ban {}".format(user))

def unban(sock, user):
    chat(sock, ".unban {}".format(user))

def timeout(sock, user, secs=300): # this 3rd argument doesn't seem to work
    chat(sock, ".timeout {}".format(user, secs))

def title(sock, title):
    # do thing

def handle(sock, name, msg):
    command, *args = msg.lower().split(" ")
    if name in MODS:
        if command == "ban":
            ban(sock, args[0])
            return
        elif command == "unban":
            unban(sock, args[0])
            return
        elif command == "timeout":
            timeout(sock, args[0], args[1]) if len(args) == 2 else timeout(sock, args[0]) # tried to do tertiary conditional but it sucks
            return
