import requests
import datetime
import pytz
from cfg import *

commands = {}
def loadCommands(*aliases):
    def decorator(function):
        for cmd in aliases:
            commands[cmd] = function
        return function
    return decorator

@loadCommands("help", "commands", "h")
def help(sock, name):
    chat(sock, "Commands: !" + ", !".join(CMDL))

@loadCommands("link", "stream", "twitch")
def twitch(sock, name):
    chat(sock, TWCH)

@loadCommands("twitter")
def twitter(sock, name):
    chat(sock, TWIT)

@loadCommands("youtube", "yt")
def youtube(sock, name):
    chat(sock, YOUT)

@loadCommands("donate", "tip")
def donate(sock, name):
    chat(sock, DNTE)

@loadCommands("time", "t", "current time", "currtime", "ct")
def currtime(sock, name):
    tz = pytz.timezone('Australia/Sydney')
    now = datetime.datetime.now(tz).strftime("%H:%M, %d %b")
    chat(sock, "Current time in Sydney is {}.".format(now))

@loadCommands("tweet", "share")
def tweet(sock, name):
    h = {
        'Accept': ACPT,
        'Client-ID': getAuth("client-id")
    }
    r = requests.get(CURL, headers=h)
    if r.status_code == requests.codes.ok:
        base = "https://www.twitter.com/share?text="
        title = dict(r.json())["status"]
        link = "&url=" + TWCH
        chat(sock, base + title + link)

@loadCommands("paizuri")
def paizuri(sock, name): 
    chat(sock, "Th-That's lewd, {} (〃▽〃)".format(name))
    if name not in MODS:
        chat(sock, ".timeout {} 300".format(name))

@loadCommands("timeout", "time", "to")
def timeout(sock, name, user, secs=300, reason=""):
    if name in MODS:
        chat(sock, ".timeout {} {} {}".format(user, secs, reason))

@loadCommands("untimeout", "untime", "uto")
def untimeout(sock, name, user):
    if name in MODS:
        chat(sock, ".untimeout {}".format(user))

@loadCommands("ban", "b", "kb")
def ban(sock, name, user):
    if name in MODS:
        chat(sock, ".ban {}".format(user))

@loadCommands("unban", "ub", "free")
def unban(sock, name, user):
    if name in MODS:
        chat(sock, ".unban {}".format(user))

@loadCommands("get")
def getIndex(sock, name, args):
    if name in MODS:
        field, *_ = args.split(' ', 1)
        if field == "title":
            field = "status"
        h = {
            'Accept': ACPT,
            'Client-ID': getAuth("client-id")
        }
        r = requests.get(CURL, headers=h)
        if r.status_code == requests.codes.ok:
            chat(sock, "Current {}: \"{}\"".format(field.capitalize(), dict(r.json())[field]))
        else:
            chat(sock, r.text)

@loadCommands("set")
def setIndex(sock, name, args):
    if name in MODS:
        field, *value = args.split(' ', 1)
        if value:
            value = value[0]
        else:
            return
        if field == "title":
            field = "status"
        h = {
            'Accept': ACPT,
            'Client-ID': getAuth("client-id"),
            'Authorization': getAuth("access-token")
        }
        d = {'channel[{}]'.format(field): value}
        r = requests.put(CURL, headers=h, data=d)
        if r.status_code == requests.codes.ok:
            chat(sock, "{} set to: \"{}\"".format(field.capitalize(), value))
        elif r.status_code == requests.codes.unauthorized:
            chat(sock, "Attempting to refresh token...")
            try:
                refreshToken()
                chat(sock, "Token refreshed, trying again.")
                r = requests.put(CURL, headers=h, data=d)
                if r.status_code == requests.codes.ok:
                    chat(sock, "{} set to: \"{}\"".format(field.capitalize(), value))
            except:
                chat(sock, "Unable to refresh token.")
        else:
            chat(sock, r.text)

def handle(sock, line):
    name = getName(line)
    msg = getMsg(line)
    print("{}: {}".format(name, msg))
    if isCommand(msg):
        cmd, *args = msg[1:].split(' ', 1)
        args = args[0] if args else None
        try:
            commands[cmd.lower()](sock, name, args)
        except:
            pass
