import discord
from discord.ext import commands

import main


class JoinRoles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        roles = main.config["join-roles"]
        for role_id in roles:
            role = member.guild.get_role(role_id)
            await member.add_roles(role)

    @commands.command(aliases=["joinrole", "join-role"])
    async def join_role(self, ctx, role: discord.Role):
        main.config["join-roles"].append(role.id)
        main.save_config()
        await ctx.send(main.replace_relevant(main.responses["join-role-success"], ctx.channel.guild).replace("%%role%%", role.name).replace("%%role(mention)%%", role.mention))

    @join_role.error
    async def join_role_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await main.send_usage(ctx, "join-role")


def setup(bot):
    bot.add_cog(JoinRoles(bot))
