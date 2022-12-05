import os
import re
import discord
import requests
from discord.ext import commands
from datetime import datetime
import schoolcalendar

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


def get_live_scores():
  rows = []
  url = "https://prod-public-api.livescore.com/v1/api/react/live/soccer/0.00?MD=1"
  jsonData = requests.get(url).json()
  for stage in jsonData['Stages']:
    if "CompId" in stage.keys():
      if stage["CompId"] in ["54", "73", "65"]:
        rows.append(stage["CompN"] + ":")
        events = stage['Events']
        for event in events:
          homeTeam = event['T1'][0]['Nm']
          homeScore = event['Tr1']

          awayTeam = event['T2'][0]['Nm']
          awayScore = event['Tr2']

          matchClock = event['Eps']

          string = "\n>\t{} - {} ({}')\t[{} - {}]".format(
            homeTeam, awayTeam, matchClock, homeScore, awayScore)
          rows.append(string)
  return rows



class SchoolCommands(commands.Cog, name="School"):
  def __init__(self, bot):
    print("School aangemaakt!")
    self.cal = schoolcalendar.SchoolCalendar()
    self.cal.open()
    self.bot = bot


  @commands.command(help="Voeg nieuw vak toe")
  async def nieuwvak(self, ctx, vak: str = commands.parameter(description="Naam toe te voegen vak")):
    self.cal.add_vak(vak)
    await ctx.send("Nieuw vak toegevoegd: **{}**".format(vak))

  @commands.command(help="Wijzig of voeg een deadline toe van een vak")
  async def setdl(self, ctx, vak: str = commands.parameter(description="Naam vak"), titel: str = commands.parameter(description="Titel van de deadline"), datum: str = commands.parameter(description="Datum van de deadline in de vorm DD/MM/YYYY"), hour: str = commands.parameter(description="Uur van de deadline in de vorm HH:MM")):
    self.cal.set_deadline(vak, ' '.join(datum, hour), titel)
    await ctx.send("Deadline voor **{}**: _{}_\n\t{}".format(vak, titel, ' '.join(datum, hour)))

  @commands.command(help="Wijzig of voeg een datum toe voor het examen van een vak")
  async def setex(self, ctx, vak: str = commands.parameter(description="Naam vak"), datum: str = commands.parameter(description="Datum van het examen in de vorm DD/MM/YYYY"), hour: str = commands.parameter(description="Uur van het examen in de vorm HH:MM")):
    self.cal.set_exam_date(vak, ' '.join(datum, hour))
    await ctx.send("Examen voor **{}**\n\t{}".format(vak, ' '.join(datum, hour)))
    
  @commands.command(help="Bekijk alle deadlines van een vak")
  async def dl(self, ctx, vak: str = commands.parameter(description="Naam vak")):
    res = "Deadlines voor **{}**:".format(vak)
    dls = self.cal.get_deadlines(vak)
    for title, date in dls.items():
      res += "\n\t{}: {}".format(date.strftime("%d/%m/%Y %H:%M"), title)
    await ctx.send(res)
    
  @commands.command(help="Bekijk alle examendata")
  async def ex(self, ctx):
    res = "**EXAMENDATA**"
    exs = self.cal.get_examens()
    for vak, date in exs.items():
      res += "\n\t{}: {}".format(date.strftime("%d/%m/%Y %H:%M"), vak)
    await ctx.send(res)

  @commands.command(help="Verwijder een vak")
  async def delvak(self, ctx, vak: str = commands.parameter(description="Naam te verwijderen vak")):
    self.cal.delete_vak(vak)
    await ctx.send("Vak **{}** verwijderd".format(vak))

  @commands.command(help="Verwijder de deadline van een vak")
  async def deldl(self, ctx, vak: str = commands.parameter(description="Naam vak"), title: str = commands.parameter(description="Naam te verwijderen deadline")):
    self.cal.delete_dl(vak, title)
    await ctx.send("Deadline __{}__ voor **{}** verwijderd".format(title, vak))
    




class BosklapperClient(commands.Bot):

  def __init__(self, command_prefix, intents,help_command):
    commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents, help_command=help_command)
    self.add_commands()

  async def on_message(self, message):
    await self.process_commands(message)
    if message.author == bot.user:
      return

    content = message.content.lower()

    if content != None:
      if "here we go" in content:
        await message.channel.send("🎵  ON THIS ROLLERCOAST LIFE WE GO! 🎶 ")

      elif "zucht" in content:
        await message.channel.send("Stop met zuchten >:(")

      elif "bier" in content:
        await message.add_reaction("🍻")

      elif "blok" in content:
        await message.add_reaction("◻️")

      elif "afspreken" in content or re.match(r"[a-z ]*spreken[a-z ]*af",
                                              content):
        with open('afspreken_guido.png', 'rb') as f:
          picture = discord.File(f)
          await message.reply(file=picture)
      
      elif "koffie" in content:
        await message.channel.send("Ja lap! We zitten met ne ring! Op ne Dusseldorf! ** GELE KAART! **")

      elif "zever" in content:
        await message.reply("GEZEVER!")

      elif "porn" in content:
        with open('porno-guido.jpg', 'rb') as f:
          picture = discord.File(f)
          await message.reply("Zijde gij ne pornomens, " + message.author.display_name + '?', file=picture)
      
      elif "satan" in content:
        with open('sammy-tanghe.jpg', 'rb') as f:
          picture = discord.File(f)
          await message.reply(file=picture)

      elif "team" in content:
        with open('blij-team.jpg', 'rb') as f:
          picture = discord.File(f)
          await message.reply(file=picture)

  async def on_ready(self):
    print('Logged in as:')
    print(bot.user.name)
    await setup(bot)
    await bot.change_presence(activity=discord.Activity(
      type=discord.ActivityType.watching, name="Het Eiland"))
      
  async def on_command_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
          await ctx.send("Ai, er ging iets mis!")

  def add_commands(self):
    @self.command(help="Ja, wa peisde nou zelf?")
    async def livescore(ctx, *args):
      live_score = get_live_scores()
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


async def setup(bot):
  await bot.add_cog(SchoolCommands(bot))


intents = discord.Intents.all()
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot = BosklapperClient(command_prefix='!', intents=intents, help_command = help_command)


bot.run(TOKEN)
