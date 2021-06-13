import asyncio
import json

import discord
from discord.ext import commands

config = json.load(open("config.json", "r"))
client = commands.Bot(command_prefix=config["prefix"])
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


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


print("Logging in...")
print("Loading Ban Extension")
client.load_extension("ban")
print("Loaded Ban Extension")
print("Loading Clear Extension")
client.load_extension("clear")
print("Loaded Clear extension")
print("Loading Prefix extension")
client.load_extension("prefix")
print("Loaded Prefix extension")
print("Loading Ping Extension")
client.load_extension("ping")
print("Loaded Ping extension")
client.run(open("token.txt", "r").read())
