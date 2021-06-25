from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

import main
from utils.math import is_int
from utils.message import replace_relevant, no_permission, send_json


class Clear(commands.Cog):

    responses = main.responses

    def __init(self, bot):
        self.bot = bot

    @commands.command(aliases=["purge"])
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount):
        if amount is None or amount == "":
            amount = 10
        if is_int(amount):
            await ctx.channel.purge(limit=int(amount)+1)
            await send_json(ctx.channel, replace_relevant(self.responses["clear-command-success"].replace("%%amount%%", str(amount)), ctx.channel.guild), delete_after=3)
        else:
            await send_json(ctx.channel, replace_relevant(self.responses["valid-integer"], ctx.channel.guild), delete_after=3)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await no_permission(ctx.message)


def setup(bot):
    bot.add_cog(Clear(bot))
