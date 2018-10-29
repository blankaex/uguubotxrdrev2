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
    # TODO
    return

def game(sock, game):
    # TODO
    return

def commands(sock):
    chat(sock, "Commands: !" + ", !".join(COMMANDS.keys()))

def currtime(sock):
    # TODO
    return

def uptime(sock):
    # TODO
    return

def command(sock, name, msg):
    command, *args = msg.lower().split()
    # can I do this "switch" better?
    if name in MODS:
        if command in MOD_COMMANDS.get("ban"):
            ban(sock, args[0])
            return
        elif command in MOD_COMMANDS.get("unban"):
            unban(sock, args[0])
            return
        elif command in MOD_COMMANDS.get("timeout"):
            timeout(sock, args[0], args[1]) if len(args) == 2 else timeout(sock, args[0]) # tried to do tertiary conditional but it sucks
            return
        elif command in MOD_COMMANDS.get("title"):
            title(sock, " ".join(args))
            return
        elif command in MOD_COMMANDS.get("game"):
            game(sock, " ".join(args))
            return
    if command in COMMANDS.get("help"):
        commands(sock)
    elif command in COMMANDS.get("link"):
        chat(sock, "https://www.twitch.tv/blankaexx")
    elif command in COMMANDS.get("twitter"):
        chat(sock, "https://twitter.com/blankaex")
    elif command in COMMANDS.get("youtube"):
        chat(sock, "https://www.youtube.com/blankaex")
    elif command == "flag":
        chat(sock, "https://blankaex.me")

def handle(sock, line):
    name = re.search(r"\w+", line).group(0)
    msg = CHAT.sub("", line).strip()
    print("{}: {}".format(name, msg))
    if msg[0] == '!':
        command(sock, name, msg[1:]) 
