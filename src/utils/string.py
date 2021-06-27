import json

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


def replace_json(json_data, repl_dict):
    data = json.dumps(json_data)

    for m in repl_dict:
        data = data.replace(m, repl_dict[m])

    return json.loads(data)


def replace_json_relevant(repl, guild):
    return replace_json(
        repl,
        {
            "%%member%%": str(round(bot.latency * 1000)),
            "%%prefix%%": str(config["prefix"]),
            "%%server%%": guild.name
        }
    )


def replace_json_member(repl, member):
    return replace_json(
        repl,
        {
            "%%member%%": f"{member.name}#{member.discriminator}",
            "%%name%%": member.name,
            "%%discriminator%%": member.discriminator,
            "%%mention%%": member.mention
        }
    )
