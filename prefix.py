from discord.ext import commands

import main


class Prefix(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prefix(self, ctx, new_prefix):
        main.config["prefix"] = new_prefix
        await ctx.send(main.replace_relevant(main.responses["prefix-command"]))


def setup(bot):
    bot.add_cog(Prefix(bot))
