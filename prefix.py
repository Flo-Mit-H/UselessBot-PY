from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

import main


class Prefix(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_permissions(manage_guild=True)
    async def prefix(self, ctx, new_prefix):
        main.config["prefix"] = new_prefix
        main.save_config()
        await ctx.send(main.replace_relevant(main.responses["prefix-command"]))

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await main.no_permission(ctx.message)


def setup(bot):
    bot.add_cog(Prefix(bot))
