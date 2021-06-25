from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

from utils.configuration import save_config
from utils.string import replace_relevant
from utils.message import no_permission, send_usage, send_json
import main


class Prefix(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_permissions(manage_guild=True)
    async def prefix(self, ctx, new_prefix):
        main.config["prefix"] = new_prefix
        save_config()
        await send_json(ctx.channel, main.responses["prefix-command"], msg=replace_relevant(main.responses["prefix-command"]["content"], ctx.guild))

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await no_permission(ctx.message)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await send_usage(ctx, "prefix")


def setup(bot):
    bot.add_cog(Prefix(bot))
