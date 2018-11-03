import datetime
from cfg import *

commands = {}
def loadCommands(*aliases):
    def decorator(function):
        for cmd in aliases:
            commands[cmd] = function
        return function
    return decorator

@loadCommands("ban", "b", "kb")
def ban(sock, name, user):
    if name in MODS:
        chat(sock, ".ban {}".format(user))

@loadCommands("unban", "ub", "free")
def unban(sock, name, user):
    if name in MODS:
        chat(sock, ".unban {}".format(user))

@loadCommands("timeout", "time", "to")
def timeout(sock, name, user, secs=300, reason=""):
    if name in MODS:
        chat(sock, ".timeout {} {} {}".format(user, secs, reason))

@loadCommands("untimeout", "untime", "uto")
def untimeout(sock, name, user):
    if name in MODS:
        chat(sock, ".untimeout {}".format(user))

@loadCommands("title")
def title(sock, name, title):
    if name in MODS:
        # TODO
        return

@loadCommands("game", "category")
def game(sock, name, game):
    if name in MODS:
        # TODO
        return

@loadCommands("help", "list", "commands")
def help(sock, name):
    chat(sock, "Commands: !" + ", !".join(CMDL))

@loadCommands("time", "t", "current time", "currtime", "ct")
def currtime(sock, name):
    print(datetime.now(tz=timezone('Australia/Sydney')))

@loadCommands("uptime", "ut")
def uptime(sock, name):
    # TODO
    return

@loadCommands("link", "stream", "streamlink", "twitch")
def link(sock, name):
    chat(sock, "https://www.twitch.tv/blankaexx")

@loadCommands("twitter", "tweet")
def twitter(sock, name):
    chat(sock, "https://twitter.com/blankaex")

@loadCommands("youtube", "yt")
def youtube(sock, name):
    chat(sock, "https://www.youtube.com/blankaex")

@loadCommands("paizuri")
def paizuri(sock, name): 
    chat(sock, "Th-that's lewd, {}".format(name))
    chat(sock, ".timeout {} 300".format(name))

def handle(sock, line):
    name = getName(line)
    msg = getMsg(line)
    print("{}: {}".format(name, msg))
    if isCommand(msg):
        cmd, *args = msg[1:].lower().split()
        try:
            commands[cmd](sock, name, *args)
        except:
            pass
