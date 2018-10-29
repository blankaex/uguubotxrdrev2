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

def command(sock, name, msg):
    command, *args = msg.lower().split()
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
        elif command == "title":
            title(sock, " ".join(args))
            return
        elif command == "game":
            game(sock, " ".join(args))
            return
    if command == "link":
        chat(sock, "https://www.twitch.tv/blankaexx")
    elif command == "twitter":
        chat(sock, "https://twitter.com/blankaex")
    elif command == "youtube":
        chat(sock, "https://www.youtube.com/blankaex")

def handle(sock, line):
    name = re.search(r"\w+", line).group(0)
    msg = CHAT.sub("", line).strip()
    print("{}: {}".format(name, msg))
    if msg[0] == '!':
        command(sock, name, msg[1:]) 
