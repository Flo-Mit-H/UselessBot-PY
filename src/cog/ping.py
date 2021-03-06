from discord.ext import commands
from utils.string import replace_relevant
import main
from utils.message import send_json


class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await send_json(ctx.channel, main.responses["ping-command"], msg=replace_relevant(main.responses["ping-command"]["content"], ctx.guild))


def setup(bot):
    bot.add_cog(Ping(bot))
