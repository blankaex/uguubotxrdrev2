import json

from twitchio.ext import commands
from api import *


class Uguu(commands.Bot):

    def __init__(self):
        self.nick = "uguubotxrdrev2"
        self.prefix = "!"
        self.initial_channels = ["blankaex"]
        self.channel_id = "41790391"

        with open("auth.json", "r") as f:
            auth = dict(json.load(f))
        self.access_token = auth.get("access-token")
        self.client_id = auth.get("client-id")
        self.client_secret = auth.get("client-secret")
        self.irc_token = auth.get("irc-token")
        self.refresh_token = auth.get("refresh-token")

        super().__init__(
            irc_token=self.irc_token,
            client_id=self.client_id,
            nick=self.nick,
            prefix=self.prefix,
            initial_channels=self.initial_channels
        )


    async def event_ready(self):
        print("Ready.")


    async def event_message(self, message):
        if not message.author.name == self.nick:
            print(message.content)
            await self.handle_commands(message)


    """
    API Commands
    """


    @commands.command(name="title")
    async def get_title(self, ctx):
        if ctx.author.is_mod:
            response = get_channel(self)
            await ctx.send(f"Current title: {response.get('status')}")


    @commands.command(name="game")
    async def get_game(self, ctx):
        if ctx.author.is_mod:
            response = get_channel(self)
            await ctx.send(f"Current game: {response.get('game')}")


    @commands.command(name="settitle")
    async def set_title(self, ctx):
        if ctx.author.is_mod:
            value = ctx.message.content.replace(f"!{ctx.command.name}", "", 1).strip()
            data = { "channel[status]": value }
            response = update_channel(self, data)
            await ctx.send(f"Title set to: {response.get('status')}")


    @commands.command(name="setgame")
    async def set_game(self, ctx):
        if ctx.author.is_mod:
            value = ctx.message.content.replace(f"!{ctx.command.name}", "", 1).strip()
            data = { "channel[game]": value }
            response = update_channel(self, data)
            await ctx.send(f"Game set to: {response.get('game')}")


    @commands.command(name="tweet")
    async def tweet(self, ctx):
        response = get_channel(self)
        content = ( "https://www.twitter.com/share"
            f"?text={response.get('status')}%20({response.get('game')})%0D%0A"
            f"&url={response.get('url')}"
        )
        await ctx.send(shorten_url(self, content))


    """
    User Commands
    """


    @commands.command(name="paizuri")
    async def paizuri(self, ctx): 
        message = f"Th-That's lewd, {ctx.author.name} (〃▽〃)"
        await ctx.send(message)
        if not ctx.author.is_mod:
            ctx.author.timeout(ctx.author.name, duration=60)
