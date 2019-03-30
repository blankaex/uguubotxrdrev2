# UguuBotXrdRev2
Twitch bot written in Python3. Namesake [Uguubot by based Infinity](https://uguubot.com/).

## Usage
The bot is (mostly) modular so you should be able to just plug in your details and be good to go. I'm assuming you don't need me to hold your hand if you want to use this.

### Steps
1. Create a Twitch account for your bot and set up an application for it.
2. Get your auth tokens and stick them in `auth.json`.
3. Fill in the relevant variables in `cfg.py` with your details.
4. Run with `$ python3 bot.py`.

### Files
* `auth.json`: Unencrypted text file containing auth tokens and such.
* `bot.py`: Main module, connects to chat and listens for commands.
* `cfg.py`: Global variables and helper methods.
* `cmd.py`: Definition and implementation of chat commands and aliases.
