from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import utils

import main
from utils.message import *


class Mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if main.config["moderation"]["ban-dm"]:
            await main.message.send_json(member, main.responses["dm-banned"], msg=replace_relevant(main.responses["dm-banned"]["content"], member.guild).replace("%%reason%%", str(reason)))
        await member.ban(reason=reason)
        await main.message.send_json(ctx.channel, main.responses["member-banned"], msg=replace_relevant(main.responses["member-banned"]["content"]
                                                                                                        .replace("%%member%%", f"{member.name}#{member.discriminator}")
                                                                                                        .replace("%%reason%%", str(reason)), ctx.channel.guild), delete_after=3)
        channel = self.bot.get_channel(main.config["moderation"]["log-channel"])
        await main.message.send_json(channel, main.responses["member-banned"], msg=replace_relevant(main.responses["member-banned"]["content"]
                                                                                                    .replace("%%member%%", f"{member.name}#{member.discriminator}")
                                                                                                    .replace("%%reason%%", str(reason)), channel.guild))

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await no_permission(ctx.message)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await send_usage(ctx, "ban")

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if main.config["moderation"]["kick-dm"]:
            await main.message.send_json(member, main.responses["dm-kicked"], msg=replace_relevant(main.responses["dm-kicked"]["content"], member.guild).replace("%%reason%%", str(reason)))
        await member.kick(reason=str(reason))
        await main.message.send_json(ctx.channel, main.responses["dm-kicked"], msg=replace_relevant(main.responses["member-kicked"]["content"]
                                                                                                    .replace("%%member%%", f"{member.name}#{member.discriminator}")
                                                                                                    .replace("%%reason%%", str(reason)), ctx.channel.guild), delete_after=3)
        channel = self.bot.get_channel(main.config["moderation"]["log-channel"])
        await main.message.send_json(member, main.responses["member-kicked"], msg=replace_relevant(main.responses["member-kicked"]["content"]
                                                                                                   .replace("%%member%%", f"{member.name}#{member.discriminator}")
                                                                                                   .replace("%%reason%%", str(reason)), channel.guild))

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await no_permission(ctx.message)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await send_usage(ctx, "kick")

    @commands.command()
    @has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await main.message.send_json(ctx.channel, main.responses["user-unbanned"], msg=replace_relevant(main.responses["user-unbanned"]["content"]
                                                                                                                .replace("%%user%%", f"{user.name}#{user.discriminator}"), ctx.guild))
                return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await no_permission(ctx.message)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await send_usage(ctx, "unban")

    @commands.command()
    @has_permissions(ban_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        muterole = main.config["moderation"]["muterole"]
        if muterole is None or muterole == "":
            await main.message.send_json(ctx.channel, main.responses["no-muterole"], msg=replace_relevant(main.responses["no-muterole"]["content"], ctx.guild))
            return
        muterole = member.guild.get_role(muterole)
        await member.add_roles(muterole)
        await main.message.send_json(ctx.channel, main.responses["member-muted"], msg=replace_relevant(main.responses["member-muted"]["content"], ctx.guild)
                                     .replace("%%member%%", f"{member.name}#{member.discriminator}").replace("%%reason%%", str(reason)), delete_after=3)
        channel = self.bot.get_channel(main.config["moderation"]["log-channel"])
        await main.message.send_json(channel, main.responses["member-muted"], msg=replace_relevant(main.responses["member-muted"]["content"], channel.guild)
                                     .replace("%%member%%", f"{member.name}#{member.discriminator}").replace("%%reason%%", str(reason)))
        if main.config["moderation"]["mute-dm"]:
            await main.message.send_json(member, main.responses["dm-muted"], msg=replace_relevant(main.responses["dm-muted"]["content"], member.guild).replace("%%reason%%", str(reason)))

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await no_permission(ctx.message)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await send_usage(ctx, "mute")

    @commands.command(aliases=["create-muterole", "create_muterole", "create-mute-role", "create_mute_role"])
    @has_permissions(manage_roles=True)
    async def createmuterole(self, ctx, name=None):
        guild = ctx.channel.guild
        muterole = await guild.create_role(name=name)
        main.config["moderation"]["muterole"] = muterole.id
        utils.configuration.save_config()
        await main.message.send_json(ctx.channel, main.responses["muterole-created"], msg=replace_relevant(main.responses["muterole-created"]["content"], ctx.guild))

    @createmuterole.error
    async def createmuterole_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await no_permission(ctx.message)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await send_usage(ctx, "createmuterole")

    @commands.command()
    @has_permissions(ban_members=True)
    async def unmute(self, ctx, member: discord.Member):
        guild = ctx.channel.guild
        muterole = main.config["moderation"]["muterole"]
        if muterole is None or muterole == "":
            await main.message.send_json(ctx.channel, main.responses["no-muterole"], msg=replace_relevant(main.responses["no-muterole"]["content"], ctx.guild))
            return
        muterole = guild.get_role(muterole)
        await member.remove_roles(muterole)
        channel = self.bot.get_channel(main.config["moderation"]["log-channel"])
        await main.message.send_json(channel, main.responses["member-unmuted"], msg=replace_relevant(main.responses["member-unmmuted"]["content"], channel.guild)
                                     .replace("%%member%%", f"{member.name}#{member.discriminator}"))
        await main.message.send_json(ctx.channel, main.responses["member-unmuted"], msg=replace_relevant(main.responses["member-unmmuted"]["content"], ctx.guild)
                                     .replace("%%member%%", f"{member.name}#{member.discriminator}"))
        if main.config["moderation"]["unmute-dm"]:
            await main.message.send_json(member, main.responses["dm-unmuted"], msg=replace_relevant(main.responses["dm-unmuted"]["content"], member.guild))

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await no_permission(ctx.message)
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await send_usage(ctx, "unmute")


def setup(bot):
    bot.add_cog(Mod(bot))
