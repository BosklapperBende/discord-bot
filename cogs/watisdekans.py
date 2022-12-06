from discord.ext import commands
import discord

class WatIsDeKans(commands.Cog, name="WatIsDeKans"):
    def __init__(self, bot):
        print("WatIsDeKans aangemaakt!")
        self.bot = bot
        self.reset_players()
        self.callback_channel = None

    def reset_players(self):
        self.player1 = None
        self.player2 = None
        self.number1 = None
        self.number2 = None
        self.max_number = None
        self.callback_channel = None
        self.started_game = False

    @commands.command(help="Start een spel")
    async def startgame(self, ctx, enemy: discord.Member = commands.parameter(description="Wie je wil uitdagen",default=None), number: int = commands.parameter(description="Maximum nummer",default=10)):
        if(self.started_game != None & self.started_game != True):
            self.reset_players()
            self.player1 = ctx.author
            self.player2 = enemy
            self.max_number = number
            self.callback_channel = ctx.message.channel
            self.started_game = True
            
            await ctx.message.channel.send("Game gestart tussen {} en {}".format(self.player1, self.player2))

            channel1 = await self.player1.create_dm()
            await channel1.send("Stuur je nummer (maximum = {})".format(self.max_number))
            channel2 = await self.player2.create_dm()
            await channel2.send("Stuur je nummer (maximum = {})".format(self.max_number))
        else:
            await ctx.message.channel.send("Er is al een game bezig tussen {} en {}".format(self.player1, self.player2))

    @commands.command(help="Stop een spel")
    async def stopgame(self, ctx):
        if self.started_game:
            if ctx.author in [self.player1, self.player2]:
                self.reset_players()
                await ctx.message.channel.send("Game gestopt")
            else:
                await ctx.message.channel.send("Enkel één van de deelnemers kan het spel stoppen, dit is {} of {}".format(self.player1, self.player2))
        else:
            await ctx.send("Is het een idee om eerst een game te starten?")

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.channel.DMChannel):
            try:
                if(message.author == self.player1):
                    self.number1 = int(message.content)
                elif(message.author == self.player2):
                    self.number2 = int(message.content)
            except ValueError:
                await message.channel.send("Geef geldig nummer")
            if(self.number1 != None & self.number2 != None):
                await self.callback_channel.send("{} zei {} en {} zei {},".format(self.player1, self.number1, self.player2, self.number2))
                self.reset_players()
