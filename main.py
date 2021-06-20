import asyncio
import json

import discord
from discord.ext import commands

config = json.load(open(file="config.json", encoding="UTF-8"))
client = commands.Bot(command_prefix=config["prefix"], intents=discord.Intents.all())
responses = config["responses"]
usages = config["usages"]

cogs = [
    "clear",
    "join_messages",
    "join_roles",
    "minecraft",
    "mod",
    "modules",
    "music",
    "ping",
    "prefix",
    "reactroles",
    "level"
]
for cog in cogs:
    print(f"Loading Extension {cog}")
    client.load_extension(cog)
    print(f"Loaded Extension {cog}")


def load_json(filename):
    with open(filename, encoding="utf-8") as infile:
        return json.load(infile)


def write_json(filename, contents):
    with open(filename, "w") as outfile:
        json.dump(contents, outfile, ensure_ascii=True, indent=4)


def save_config():
    write_json("config.json", config)


@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}#{client.user.discriminator}")
    print("Initializing Update Task")
    client.loop.create_task(update_task())
    print("Initialized Update Task")
    print("Initializing Status Task")
    client.loop.create_task(staus_task())
    print("Intialized Status Task")


async def staus_task():
    while True:
        for i in range(len(config["rich-presence"]["states"])):

            # Activity
            activity = discord.Game(config["rich-presence"]["states"][i]["message"])

            # Status
            statusstr = config["rich-presence"]["states"][i]["status"]
            status = discord.Status.online
            if statusstr == "idle":
                status = discord.Status.idle
            elif statusstr == "dnd" or statusstr == "do_not_disturb":
                status = discord.Status.do_not_disturb
            elif statusstr == "offline" or statusstr == "Offline":
                status = discord.Status.offline

            await client.change_presence(activity=activity, status=status, afk=config["rich-presence"]["states"][i]["afk"])
            await asyncio.sleep(config["rich-presence"]["delay"])


async def update_task():
    while True:
        client.command_prefix = config["prefix"]
        await asyncio.sleep(1)


def replace_relevant(repl, guild):
    repl = repl \
        .replace("%%ping%%", str(round(client.latency * 1000))) \
        .replace("%%prefix%%", str(config["prefix"])) \
        .replace("%%server%%", guild.name)
    return repl


def replace_member(s, member: discord.Member):
    s = s \
        .replace("%%member%%", f"{member.name}#{member.discriminator}") \
        .replace("%%name%%", member.name) \
        .replace("%%discriminator%%", member.discriminator) \
        .replace("%%mention%%", member.mention)
    return s


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


async def no_permission(message: discord.Message):
    await message.reply(replace_relevant(responses["no-permission"], message.channel.guild))


async def send_usage(ctx, name):
    await ctx.send(replace_relevant(usages[f"{name}-usage"], ctx.guild))


client.run(open("token.txt", "r").read())
