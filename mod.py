import discord
from discord.ext import commands

import main


class Mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if main.config["ban-dm"]:
            await member.send(main.replace_relevant(main.responses["dm-banned"]).replace("%%reason%%", str(reason)))
        await member.ban(reason=reason)
        await ctx.channel.send(main.replace_relevant(main.responses["member-banned"].replace("%%member%%", f"{member.name}#{member.discriminator}")
                                                     .replace("%%reason%%", str(reason))), delete_after=3)
        channel = self.bot.get_channel(main.config["log-channel"])
        await channel.send(main.replace_relevant(main.responses["member-banned"].replace("%%member%%", f"{member.name}#{member.discriminator}")
                                                 .replace("%%reason%%", str(reason))))

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if main.config["kick-dm"]:
            await member.send(main.replace_relevant(main.responses["dm-kicked"]).replace("%%reason%%", str(reason)))
        await member.kick(reason=str(reason))
        await ctx.channel.send(main.replace_relevant(main.responses["member-kicked"].replace("%%member%%", f"{member.name}#{member.discriminator}")
                                                     .replace("%%reason%%", str(reason))), delete_after=3)
        channel = self.bot.get_channel(main.config["log-channel"])
        await channel.send(main.replace_relevant(main.responses["member-kicked"].replace("%%member%%", f"{member.name}#{member.discriminator}")
                                                 .replace("%%reason%%", str(reason))))

    @commands.command()
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(main.replace_relevant(main.responses["user-unbanned"].replace("%%user%%", f"{user.name}#{user.discriminator}")))
                return


def setup(bot):
    bot.add_cog(Mod(bot))
