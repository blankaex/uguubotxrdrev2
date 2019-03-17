import requests
import datetime
import pytz
import shlex
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

@loadCommands("get")
def get(sock, name, index):
    if name in MODS:
        arg = "status" if index == "title" else index
        h = {'Accept': ACPT, 'Client-ID': CLID}
        r = requests.get(CURL, headers=h)
        if r.status_code == requests.codes.ok:
            chat(sock, "Current {}: \"{}\"".format(index[0].upper() + index[1:], dict(r.json())[arg]))
        else:
            chat(sock, "Invalid command")
        return

@loadCommands("set")
def game(sock, name, index, value):
    if name in MODS:
        arg = "status" if index == "title" else index
        h = {'Accept': ACPT, 'Client-ID': CLID, 'Authorization': AUTH}
        d = {'channel[{}]'.format(arg): value}
        r = requests.put(CURL, headers=h, data=d)
        if r.status_code == requests.codes.ok:
            chat(sock, "{} set to: \"{}\"".format(index[0].upper() + index[1:], value))
        else:
            chat(sock, "Invalid command")
        return

@loadCommands("help", "commands", "h")
def help(sock, name):
    chat(sock, "Commands: !" + ", !".join(CMDL))

@loadCommands("time", "t", "current time", "currtime", "ct")
def currtime(sock, name):
    tz = pytz.timezone('Australia/Sydney')
    now = datetime.datetime.now(tz).strftime("%H:%M, %d %b")
    chat(sock, "Current time in Sydney is {}.".format(now))

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
    chat(sock, "Th-That's lewd, {} (〃▽〃)".format(name))
    if name not in MODS:
        chat(sock, ".timeout {} 300".format(name))

def handle(sock, line):
    name = getName(line)
    msg = getMsg(line)
    print("{}: {}".format(name, msg))
    if isCommand(msg):
        cmd, *args = shlex.split(msg[1:])
        try:
            commands[cmd.lower()](sock, name, *args)
        except:
            pass
