import asyncio
import json

import discord
from discord.ext import commands

config = json.load(open("config.json", "r"))
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=config["prefix"], intents=intents)
responses = config["responses"]


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


def replace_relevant(repl):
    repl = repl\
        .replace("%%ping%%", str(round(client.latency * 1000)))\
        .replace("%%prefix%%", str(config["prefix"]))
    return repl


def replace_member(s, member: discord.Member):
    s = s\
        .replace("%%member%%", f"{member.name}#{member.discriminator}")\
        .replace("%%name%%", member.name)\
        .replace("%%discriminator%%", member.discriminator)\
        .replace("%%mention%%", member.mention)
    return s


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


async def no_permission(message: discord.Message):
    await message.reply(replace_relevant(responses["no-permission"]))


print("Loading Mod Commands")
client.load_extension("mod")
print("Loaded Mod Commands")
print("Loading Clear Command")
client.load_extension("clear")
print("Loaded Clear Command")
print("Loading Prefix Command")
client.load_extension("prefix")
print("Loaded Prefix Command")
print("Loading Ping Command")
client.load_extension("ping")
print("Loaded Ping Command")
print("Loading Minecraft Console Extension")
client.load_extension("minecraft")
print("Loaded Minecraft Console Extension")
print("Loading Join Messages Extension")
client.load_extension("join-messages")
print("Loaded Join Messages Extensions")
print("Logging in...")
client.run(open("token.txt", "r").read())
