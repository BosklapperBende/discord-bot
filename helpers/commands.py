import discord
import re

async def react_to_message(message: discord.Message):
    content = message.content.lower()

    if content == None:
        return

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
        with open('img/afspreken_guido.png', 'rb') as f:
            picture = discord.File(f)
            await message.reply(file=picture)
    
    elif "koffie" in content:
        await message.channel.send("Ja lap! We zitten met ne ring! Op ne Dusseldorf! ** GELE KAART! **")

    elif "zever" in content:
        await message.reply("GEZEVER!")

    elif "porn" in content:
        with open('img/porno-guido.jpg', 'rb') as f:
            picture = discord.File(f)
            await message.reply("Zijde gij ne pornomens, " + message.author.display_name + '?', file=picture)
    
    elif "satan" in content:
        with open('img/sammy-tanghe.jpg', 'rb') as f:
            picture = discord.File(f)
            await message.reply(file=picture)

    elif "team" in content:
        with open('img/blij-team.jpg', 'rb') as f:
            picture = discord.File(f)
            await message.reply(file=picture)