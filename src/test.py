import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=":?", intents=discord.Intents.all())


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    embed = discord.Embed(title="Hay")

    await message.channel.send(embed=embed)


@bot.event
async def on_ready():
    print(f"Bot logged in as User {bot.user.name}#{bot.user.discriminator}")


bot.run("ODUzNTkxNDk2MTAzMTY1OTYy.YMXnBw.w_2K4augRcW52JUVEexlrHqaZGs")
