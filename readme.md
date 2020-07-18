# UguuBotXrdRev2
Twitch bot written in Python3. Namesake [Uguubot by based Infinity](https://uguubot.com/). Maybe it should be UguuBotStrive now?

The goal was mainly to be able to interface with the Twitch API via IRC, so I wouldn't have to deal with the annoying GUI.

## Usage
The bot is (mostly) modular so you should be able to just plug in your details and be good to go. I'm assuming you don't need me to hold your hand if you want to use this.

### Steps
1. Create a Twitch account for your bot and set up an application for it.
2. Get your auth tokens and stick them in `auth.json`.
3. Update the relevant instance variables in `bot.py` with your details.
4. Run `main.py`.

### Getting an OAuth token:
If the token expires and won't refresh for some reason, make this GET request (in a browser):
```
https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=<CLIENT ID>&redirect_uri=http://localhost&scope=channel_editor
```
The request will redirect you to `localhost` with the tokens as GET parameters.

## Commands
| **Command**       | **Description**             |
|-------------------|-----------------------------|
| `!title`          | Fetch current stream title. |
| `!settitle TITLE` | Set stream title to TITLE.  |
| `!game`           | Fetch current game.         |
| `!setgame GAME`   | Set game to GAME.           |
| `!tweet`          | Posts link to tweet stream. |
| `!paizuri`        | What are you doing?         |
