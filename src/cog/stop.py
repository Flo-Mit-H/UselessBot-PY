from discord.ext import commands
import discord


class Stop(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def die(self, ctx):
        user_id = ctx.message.author.id
        if user_id == 498515383934779392 or user_id == 415208974602862593:
            await self.bot.change_presence(status=discord.Status.offline)
            exit(1)
        else:
            ctx.send("Das darfst du nicht!")


def setup(bot):
    bot.add_cog(Stop(bot))
