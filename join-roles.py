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

    @commands.command(aliases=["joinrole"])
    async def join_role(self, ctx, role: discord.Role):
        main.config["join-roles"].append(role.id)
        main.write_json("newconfig.json", main.config)
        await ctx.send(main.replace_relevant(main.responses["join-role-success"]).replace("%%role%%", role.name).replace("%%role(mention)%%", role.mention))


def setup(bot):
    bot.add_cog(JoinRoles(bot))
