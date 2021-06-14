from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

import main


class Clear(commands.Cog):

    responses = main.responses

    def __init(self, bot):
        self.bot = bot

    @commands.command(aliases=["purge"])
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount):
        if amount is None or amount == "":
            amount = 10
        if main.is_int(amount):
            await ctx.channel.purge(limit=int(amount)+1)
            await ctx.send(main.replace_relevant(self.responses["clear-command-success"].replace("%%amount%%", str(amount))), delete_after=3)
        else:
            await ctx.send(main.replace_relevant(self.responses["valid-integer"]), delete_after=3)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await main.no_permission(ctx.message)


def setup(bot):
    bot.add_cog(Clear(bot))
