import logging
import os
import discord
from discord.ext import commands, tasks
import cogs
from datetime import datetime, time, timedelta
import asyncio
import random as rn
import helpers
from dotenv import load_dotenv

helpers.setup_logger()

_log = logging.getLogger(__name__)

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GITHUB_TOKEN = os.getenv("GH_TOKEN")

class BosklapperClient(commands.Bot):

  def __init__(self, command_prefix, intents,help_command):
    commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents, help_command=help_command)
    self.add_commands()
    self.reminder_channel = None
    self.joke_channel = None

  async def on_message(self, message):
    await self.process_commands(message)
    if message.author == bot.user:
      return
    
    await helpers.react_to_message(message)

  async def on_ready(self):
    _log.info("Started Bosklapper Bot...")
    await self.setup()
    await self.change_presence(activity=discord.Activity(
      type=discord.ActivityType.watching, name="Het Eiland"))
    self.reminders.start()
    self.joke.start()

  async def setup(self):
    self.schoolcom = cogs.SchoolCommands(self)
    await self.add_cog(cogs.WatIsDeKans(self))
    await self.add_cog(cogs.Github(self, GITHUB_TOKEN))
    await self.add_cog(self.schoolcom)
      
  async def on_command_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send("Ai, er ging iets mis!")

  @tasks.loop(hours=7*24)
  async def reminders(self):
    try:
      now = datetime.utcnow()
      await self.schoolcom.send_upcoming_dl(self.get_channel(self.reminder_channel))
      tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
      seconds = (tomorrow - now).total_seconds()  
      await asyncio.sleep(seconds) 
    except NameError:
      print("Geen gevonden")

  @reminders.before_loop  # it's called before the actual task runs
  async def before_reminders(self):
    await self.wait_until_ready()
    await helpers.wait_until_time(8, True)

  @tasks.loop(seconds=10)
  async def joke(self):
    if self.joke_channel == None:
      return
    try:
      now = datetime.utcnow()
      cat, joke = helpers.get_joke()
      await self.get_channel(self.joke_channel).send("**Mop van de dag: *** Het is een _{}_\n```{}```".format(cat, joke))
      tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
      seconds = (tomorrow - now).total_seconds()  
      await asyncio.sleep(seconds) 
    except NameError:
      print("Geen gevonden")

  @joke.before_loop
  async def before_joke(self):
    await self.wait_until_ready()
    await helpers.wait_until_time(12)

  def add_commands(self):
    @self.command(help="Ja, wa peisde nou zelf?")
    async def livescore(ctx, *args):
      live_score = helpers.get_live_scores()
      if len(live_score) == 0:
        await ctx.send(
          "Ai, jammer. Er worden momenteel geen wedstrijden gespeeld.")
      else:
        for game in live_score:
          await ctx.send(game)

    @self.command(help="Ahja, omgekeerd praten gelijk de sammy he! Das keicool")
    async def rev(ctx, *args):
      args_n = []
      for arg in args:
        args_n.append(arg[::-1])
      await ctx.send(' '.join(args_n))

    @self.command(help="Ahja, omgekeerd praten ma nu NEXT LEVEL")
    async def fullrev(ctx, *args):
      args_n = []
      for arg in args[::-1]:
        args_n.append(arg[::-1])
      await ctx.send(' '.join(args_n))

    @self.command(help="Wijzig het kanaal voor de reminders")
    async def setremch(ctx, arg):
      self.reminder_channel = int(arg)
      await ctx.send("Reminders worden nu gestuurd in kanaal: **{}**".format(self.get_channel(self.reminder_channel)))

    @self.command(help="Wijzig het kanaal voor de moppen")
    async def setjokech(ctx, arg):
      self.joke_channel = int(arg)
      await ctx.send("De dagelijkse mop wordt nu gestuurd in kanaal: **{}**".format(self.get_channel(self.joke_channel)))

    @self.command(help="Kies een random persoon uit de server")
    async def random(ctx):
      members = [ member for member in ctx.guild.members if not member.bot]
      random_member = rn.choice(members)
      await ctx.send("Tromgeroffel...")
      await asyncio.sleep(2)
      await ctx.send("▶️ <@{}> ◀️".format(random_member.id))

intents = discord.Intents.all()
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot = BosklapperClient(command_prefix='!', intents=intents, help_command = help_command)


bot.run(DISCORD_TOKEN, log_handler=None)