from discord.ext import commands
import main


class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(main.replace_relevant(main.responses["ping-command"], ctx.guild))


def setup(bot):
    bot.add_cog(Ping(bot))
