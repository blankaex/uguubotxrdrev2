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
def getIndex(sock, name, index):
    if name in MODS:
        arg = "status" if index == "title" else index
        h = {'Accept': ACPT, 'Client-ID': CLID}
        r = requests.get(CURL, headers=h)
        if r.status_code == requests.codes.ok:
            chat(sock, "Current {}: \"{}\"".format(index[0].upper() + index[1:], dict(r.json())[arg]))
        else:
            chat(sock, r.text)

@loadCommands("set")
def setIndex(sock, name, index, value):
    if name in MODS:
        arg = "status" if index == "title" else index
        h = {'Accept': ACPT, 'Client-ID': CLID, 'Authorization': AUTH}
        d = {'channel[{}]'.format(arg): value}
        r = requests.put(CURL, headers=h, data=d)
        if r.status_code == requests.codes.ok:
            chat(sock, "{} set to: \"{}\"".format(index[0].upper() + index[1:], value))
        elif r.status_code == requests.codes.unauthorized:
            chat(sock, "Attempting to refresh token...")
            try:
                refreshToken()
                chat(sock, "Token refreshed.")
                setIndex(sock, name, index, value)
            except:
                chat(sock, "Unable to refresh token.")
        else:
            chat(sock, r.text)

@loadCommands("help", "commands", "h")
def help(sock, name):
    chat(sock, "Commands: !" + ", !".join(CMDL))

@loadCommands("time", "t", "current time", "currtime", "ct")
def currtime(sock, name):
    tz = pytz.timezone('Australia/Sydney')
    now = datetime.datetime.now(tz).strftime("%H:%M, %d %b")
    chat(sock, "Current time in Sydney is {}.".format(now))

@loadCommands("tweet", "share")
def tweet(sock, name):
    h = {'Accept': ACPT, 'Client-ID': CLID}
    r = requests.get(CURL, headers=h)
    if r.status_code == requests.codes.ok:
        chat(sock, "https://www.twitter.com/share?text=" + dict(r.json())["status"] + "&url=https://www.twitch.tv/blankaexx")

@loadCommands("link", "stream", "twitch")
def twitch(sock, name):
    chat(sock, TWCH)

@loadCommands("twitter")
def twitter(sock, name):
    chat(sock, TWIT)

@loadCommands("youtube", "yt")
def youtube(sock, name):
    chat(sock, YOUT)

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
