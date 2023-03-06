import logging
import pickle
from discord.ext import commands
import discord
import random as rn
import asyncio
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import os

_log = logging.getLogger(__name__)

class Custom(commands.Cog, name="Custom"):
    def __init__(self, bot):
        _log.info("Commands created")
        self.bot = bot
        self.channels = {
          "reminders": None,
          "joke": None
        }
        for guild in bot.guilds:
          self.open_channels_file(guild.id)
        

    def open_channels_file(self, guild_id):
      try:
          if(not os.path.exists(f"/saved/channels{guild_id}.pkl")):
              file = open(f'/saved/channels{guild_id}.pkl','wb+')
              _log.info("Creating new file for this guild")
              pickle.dump(self.channels,file)
              file.close()
          else:
              _log.info(f"Restoring backup for guild{guild_id}")
              
      except Exception as e:
          _log.error("{} - {}".format(type(e), e))

      with open(f'/saved/channels{guild_id}.pkl','rb') as input:
          self.channels = pickle.load(input)

    def write_channels_to_file(self, ctx):
      with open(f"saved/channels{ctx.guild.id}.pkl", "wb") as out:
        pickle.dump(self.deadlines, out, pickle.HIGHEST_PROTOCOL)
        

    @commands.command(help="Sla iemand")
    async def punch(self, ctx, punched: discord.Member = commands.parameter(description="Wie je wil slaan",default=None)):
        await ctx.send(f"**MATS!** <@{ctx.author.id}> heeft <@{punched.id}> geslagen.")

    @commands.command(help="Ja, wa peisde nou zelf?")
    async def livescore(self, ctx):
      live_score = self.helpers.get_live_scores()
      if len(live_score) == 0:
        await ctx.send(
          "Ai, jammer. Er worden momenteel geen wedstrijden gespeeld.")
      else:
        for game in live_score:
          await ctx.send(game)

    @commands.command(help="Ahja, omgekeerd praten gelijk de sammy he! Das keicool")
    async def rev(self, ctx, *args):
      args_n = []
      for arg in args:
        args_n.append(arg[::-1])
      await ctx.send(' '.join(args_n))

    @commands.command(help="Ahja, omgekeerd praten ma nu NEXT LEVEL")
    async def fullrev(self, ctx, *args):
      args_n = []
      for arg in args[::-1]:
        args_n.append(arg[::-1])
      await ctx.send(' '.join(args_n))

    @commands.command(help="Wijzig het kanaal voor de reminders")
    async def setremch(self, ctx, arg):
      self.channels["reminders"] = int(arg)
      self.write_channels_to_file(ctx)
      await ctx.send("Reminders worden nu gestuurd in kanaal: **{}**".format(self.get_channel(self.channels["reminders"])))

    @commands.command(help="Wijzig het kanaal voor de moppen")
    async def setjokech(self, ctx, arg):
      self.channels["joke"] = int(arg)
      self.write_channels_to_file(ctx)
      await ctx.send("De dagelijkse mop wordt nu gestuurd in kanaal: **{}**".format(self.get_channel(self.channels["joke"])))

    @commands.command(help="Kies een random persoon uit de server")
    async def random(self, ctx):
      members = [ member for member in ctx.guild.members if not member.bot]
      random_member = rn.choice(members)
      await ctx.send("Tromgeroffel...")
      await asyncio.sleep(2)
      await ctx.send("▶️ <@{}> ◀️".format(random_member.id))

    @commands.command(help="Speel het legendarische nummer in huidige voice channel")
    async def rollercoaster(self, ctx):
      channel = ctx.message.author.voice.channel
      if not channel:
          await ctx.send(f"{ctx.message.author.name} zit niet in een voice channel.")
          return
      else:
          try:
              voice = ctx.message.author.guild.voice_client
              if voice and voice.is_connected():
                  await voice.move_to(channel)
              else:
                await channel.connect()
                voice = ctx.message.author.guild.voice_client
              
              location = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir)+"/music/rollercoaster.mp3")
              voice.play(discord.FFmpegPCMAudio(location),
                          after=lambda _: asyncio.run_coroutine_threadsafe(
                              coro=voice.disconnect(),
                              loop=voice.loop
                          ).result())
              voice.source = discord.PCMVolumeTransformer(voice.source)
              voice.source.volume = 0.15
          except Exception as e:
              _log.error(e)