import discord

from main import bot, config


def replace_relevant(repl, guild):
    repl = repl \
        .replace("%%ping%%", str(round(bot.latency * 1000))) \
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