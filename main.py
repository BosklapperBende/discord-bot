import logging
import os
import pickle
import discord
from discord.ext import commands, tasks
import cogs
from datetime import datetime, time, timedelta
import asyncio
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

  async def on_message(self, message):
    await self.process_commands(message)
    if message.author == bot.user:
      return
    
    await helpers.react_to_message(self, message)

  async def on_ready(self):
    _log.info("Started Bosklapper Bot...")
    await self.setup()
    await self.change_presence(activity=discord.Activity(
      type=discord.ActivityType.watching, name="Het Eiland"))
    self.reminders.start()
    self.joke.start()
    #await self.send_updates()

  async def setup(self):
    self.schoolcom = cogs.SchoolCommands(self)
    self.customcog = cogs.Custom(self)
    await self.add_cog(cogs.WatIsDeKans(self))
    await self.add_cog(cogs.Github(self, GITHUB_TOKEN))
    await self.add_cog(self.schoolcom)
    await self.add_cog(self.customcog)
      
  async def on_command_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send("Ai, er ging iets mis!")

  @tasks.loop(hours=7*24)
  async def reminders(self):
    try:
      now = datetime.utcnow()
      await self.schoolcom.send_upcoming_dl(self.get_channel(self.customcog.channels["reminders"]))
      tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
      seconds = (tomorrow - now).total_seconds()  
      await asyncio.sleep(seconds) 
    except NameError:
      print("Geen gevonden")

  @reminders.before_loop  # it's called before the actual task runs
  async def before_reminders(self):
    await self.wait_until_ready()
    await helpers.wait_until_time(9, True)

  @tasks.loop(hours=24)
  async def joke(self):
    if self.customcog.channels["joke"] == None:
      return
    try:
      now = datetime.utcnow()
      cat, joke = helpers.get_joke()
      await self.get_channel(self.customcog.channels["joke"]).send("**Mop van de dag: ** Het is een _{}_\n```{}```".format(cat, joke))
      tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
      seconds = (tomorrow - now).total_seconds()  
      await asyncio.sleep(seconds) 
    except NameError:
      print("Geen gevonden")

  @joke.before_loop
  async def before_joke(self):
    await self.wait_until_ready()
    await helpers.wait_until_time(11)

  async def send_updates(self):
    with open("updates.txt") as f:
      for guild in self.guilds:
          channel = guild.system_channel 
          if guild.id == 1033379492904837121:
            await channel.send(f.read())
     

intents = discord.Intents.all()
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot = BosklapperClient(command_prefix='!', intents=intents, help_command = help_command)


bot.run(DISCORD_TOKEN, log_handler=None)