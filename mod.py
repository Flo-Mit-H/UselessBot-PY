import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

import main


class Mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if main.config["moderation"]["ban-dm"]:
            await member.send(main.replace_relevant(main.responses["dm-banned"], member.guild).replace("%%reason%%", str(reason)))
        await member.ban(reason=reason)
        await ctx.channel.send(main.replace_relevant(main.responses["member-banned"].replace("%%member%%", f"{member.name}#{member.discriminator}")
                                                     .replace("%%reason%%", str(reason)), ctx.channel.guild), delete_after=3)
        channel = self.bot.get_channel(main.config["moderation"]["log-channel"])
        await channel.send(main.replace_relevant(main.responses["member-banned"].replace("%%member%%", f"{member.name}#{member.discriminator}")
                                                 .replace("%%reason%%", str(reason)), channel.guild))

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await main.no_permission(ctx.message)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await main.send_usage(ctx, "ban")

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if main.config["moderation"]["kick-dm"]:
            await member.send(main.replace_relevant(main.responses["dm-kicked"], member.guild).replace("%%reason%%", str(reason)))
        await member.kick(reason=str(reason))
        await ctx.channel.send(main.replace_relevant(main.responses["member-kicked"].replace("%%member%%", f"{member.name}#{member.discriminator}")
                                                     .replace("%%reason%%", str(reason)), ctx.channel.guild), delete_after=3)
        channel = self.bot.get_channel(main.config["moderation"]["log-channel"])
        await channel.send(main.replace_relevant(main.responses["member-kicked"].replace("%%member%%", f"{member.name}#{member.discriminator}")
                                                 .replace("%%reason%%", str(reason)), channel.guild))

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await main.no_permission(ctx.message)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await main.send_usage(ctx, "kick")

    @commands.command()
    @has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(main.replace_relevant(main.responses["user-unbanned"].replace("%%user%%", f"{user.name}#{user.discriminator}"), ctx.guild))
                return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await main.no_permission(ctx.message)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await main.send_usage(ctx, "unban")

    @commands.command()
    @has_permissions(ban_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        muterole = main.config["moderation"]["muterole"]
        if muterole is None or muterole == "":
            await ctx.channel.send(main.replace_relevant(main.responses["no-muterole"], ctx.guild))
            return
        muterole = member.guild.get_role(muterole)
        await member.add_roles(muterole)
        await ctx.channel.send(main.replace_relevant(main.responses["member-muted"], ctx.guild).replace("%%member%%", f"{member.name}#{member.discriminator}")
                               .replace("%%reason%%", str(reason)), delete_after=3)
        channel = self.bot.get_channel(main.config["moderation"]["log-channel"])
        await channel.send(main.replace_relevant(main.responses["member-muted"], channel.guild).replace("%%member%%", f"{member.name}#{member.discriminator}")
                           .replace("%%reason%%", str(reason)))
        if main.config["moderation"]["mute-dm"]:
            await member.send(main.replace_relevant(main.responses["dm-muted"], member.guild).replace("%%reason%%", str(reason)))

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await main.no_permission(ctx.message)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await main.send_usage(ctx, "mute")

    @commands.command(aliases=["create-muterole", "create_muterole", "create-mute-role", "create_mute_role"])
    @has_permissions(manage_roles=True)
    async def createmuterole(self, ctx, name=None):
        guild = ctx.channel.guild
        muterole = await guild.create_role(name=name)
        main.config["moderation"]["muterole"] = muterole.id
        main.save_config()
        await ctx.channel.send(main.replace_relevant(main.responses["muterole-created"], ctx.guild))

    @createmuterole.error
    async def createmuterole_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await main.no_permission(ctx.message)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await main.send_usage(ctx, "createmuterole")

    @commands.command()
    @has_permissions(ban_members=True)
    async def unmute(self, ctx, member: discord.Member):
        guild = ctx.channel.guild
        muterole = main.config["moderation"]["muterole"]
        if muterole is None or muterole == "":
            await ctx.channel.send(main.replace_relevant(main.responses["no-muterole"], ctx.guild))
            return
        muterole = guild.get_role(muterole)
        await member.remove_roles(muterole)
        channel = self.bot.get_channel(main.config["moderation"]["log-channel"])
        await channel.send(main.replace_relevant(main.responses["member-unmmuted"], channel.guild).replace("%%member%%", f"{member.name}#{member.discriminator}"))
        await ctx.channel.send(main.replace_relevant(main.responses["member-unmmuted"], ctx.guild).replace("%%member%%", f"{member.name}#{member.discriminator}"))
        if main.config["moderation"]["unmute-dm"]:
            await member.send(main.replace_relevant(main.responses["dm-unmuted"], member.guild))

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await main.no_permission(ctx.message)
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await main.send_usage(ctx, "unmute")


def setup(bot):
    bot.add_cog(Mod(bot))
