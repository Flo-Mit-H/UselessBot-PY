import json
from math import floor

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

from utils.string import *
from utils.message import *
import main


def is_user_exists(userdata, user):
    try:
        return userdata[str(user.id)] is not None
    except KeyError:
        return False


async def check_level_up(lvl, message, xp, member: discord.Member):
    levels = list(main.config["leveling"]["level"])
    for i in range(len(main.config["leveling"]["level"])):
        level = main.config["leveling"]["level"][levels[i]]
        if lvl == level:
            role = discord.utils.get(member.guild.roles, name=levels[i])
            if role in member.roles:
                return
            await member.add_roles(role)
            msg = replace_relevant(main.responses["leveled-up-with-role"], message.guild)
            msg = replace_member(msg, member)
            msg = msg.replace("%%role%%", role.name).replace("%%role.mention%%", role.mention) \
                .replace("%%level%%", str(lvl))
            return await main.message.send_json(message.channel, main.responses["leveled-up-with-role"], msg=msg)
    if xp == 0:
        msg = replace_relevant(main.responses["leveled-up"], message.guild)
        msg = replace_member(msg, member).replace("%%level%%", str(lvl))
        await main.message.send_json(message.channel, main.responses["leveled-up"], msg=msg)


async def send_success_message(msg, member, level, userdata, ctx, _json):
    msg = replace_member(msg, member)
    msg = msg.replace("%%level%%", str(level))
    await main.message.send_json(ctx.channel, _json, msg=msg)

    xp = userdata[str(member.id)]
    lvl = floor(xp / 100)
    xp -= lvl * 100
    await check_level_up(lvl, ctx.message, xp, member)


async def remove_roles(member):
    levels = list(main.config["leveling"]["level"])
    for i in range(len(main.config["leveling"]["level"])):
        role = discord.utils.get(member.guild.roles, name=levels[i])
        if role in member.roles:
            await member.remove_roles(role)


class LevelingSystem(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        with open("../../config/level-user.json", "r") as file:
            userdata = json.load(file)

        if not is_user_exists(userdata, message.author):
            userdata[str(message.author.id)] = 100
        else:
            userdata[str(message.author.id)] += 5
            xp = userdata[str(message.author.id)]
            lvl = floor(xp / 100)
            xp -= lvl * 100
            await check_level_up(lvl, message, xp, message.author)

        with open("../../config/level-user.json", "w") as file:
            json.dump(userdata, file)

    # noinspection PyTypeChecker
    # no inspection above bc PyCharm said member.id doesn´t exist -> https://discordpy.readthedocs.io/en/stable/api.html?highlight=message%20author#discord.Member.id
    @commands.command(aliases=["add-level"])
    @has_permissions(manage_roles=True)
    async def add_level(self, ctx, member: discord.Member, level: int):
        with open("../../config/level-user.json", "r") as file:
            userdata = json.load(file)

        if not is_user_exists(userdata, member):
            userdata[str(member.id)] = level * 100
        else:
            userdata[str(member.id)] += level * 100
        msg = replace_relevant(main.responses["added-level"], member.guild)
        msg = replace_member(msg, member)
        await send_success_message(msg, member, level, userdata, ctx, main.responses["added-level"])

        with open("../../config/level-user.json", "w") as file:
            json.dump(userdata, file)

    @add_level.error
    async def add_level_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await send_usage(ctx, "add-level")
        elif isinstance(error, MissingPermissions):
            await no_permission(ctx.message)

    # noinspection PyTypeChecker
    # no inspection above bc PyCharm said member.id doesn´t exist -> https://discordpy.readthedocs.io/en/stable/api.html?highlight=message%20author#discord.Member.id
    @commands.command(aliases=["remove-level"])
    @has_permissions(manage_roles=True)
    async def remove_level(self, ctx, member: discord.Member, level: int):
        with open("../../config/level-user.json", "r") as file:
            userdata = json.load(file)
        if not is_user_exists(userdata, member):
            userdata[str(member.id)] = 0
        else:
            userdata[str(member.id)] -= level * 100
        msg = replace_relevant(main.responses["removed-level"], member.guild)
        await remove_roles(member)
        await send_success_message(msg, member, level, userdata, ctx, main.responses["remove-level"])

        with open("../../config/level-user.json", "w") as file:
            json.dump(userdata, file)

    @remove_level.error
    async def remove_level_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await send_usage(ctx, "remove-level")
        elif isinstance(error, MissingPermissions):
            await no_permission(ctx.message)

    # noinspection PyTypeChecker
    # no inspection above bc PyCharm said member.id doesn´t exist -> https://discordpy.readthedocs.io/en/stable/api.html?highlight=message%20author#discord.Member.id
    @commands.command(aliases=["reset-level"])
    @has_permissions(manage_roles=True)
    async def reset_level(self, ctx, member: discord.Member):
        with open("../../config/level-user.json", "r") as file:
            userdata = json.load(file)

        if is_user_exists(userdata, member):
            userdata[str(member.id)] = 0

        await remove_roles(member)
        msg = replace_relevant(main.responses["reset-level"], member.guild)
        msg = replace_member(msg, member)
        await main.message.send_json(ctx.channel, main.responses["reset-level"], msg=msg)
        with open("../../config/level-user.json", "w") as file:
            json.dump(userdata, file)

    @reset_level.error
    async def reset_level_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await send_usage(ctx, "reset-level")
        elif isinstance(error, MissingPermissions):
            await no_permission(ctx.message)


def setup(_bot):
    _bot.add_cog(LevelingSystem(_bot))
