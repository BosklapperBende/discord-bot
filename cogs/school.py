import schoolcalendar
from discord.ext import commands

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
    