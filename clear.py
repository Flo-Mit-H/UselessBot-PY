from discord.ext import commands

import main


class Clear(commands.Cog):

    responses = main.responses

    def __init(self, bot):
        self.bot = bot

    @commands.command(aliases=["purge"])
    async def clear(self, ctx, amount):
        if amount is None or amount == "":
            amount = 10
        if main.is_int(amount):
            await ctx.channel.purge(limit=int(amount)+1)
            await ctx.send(main.replace_relevant(self.responses["clear-command-success"].replace("%%amount%%", str(amount))), delete_after=3)
        else:
            await ctx.send(main.replace_relevant(self.responses["valid-integer"]), delete_after=3)


def setup(bot):
    bot.add_cog(Clear(bot))
