from discord.ext import commands

import main


class JoinMessages(commands.Cog):
    join_message = main.config["join-message"]

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(self.join_message["join-channel"])
        message = main.replace_relevant(self.join_message["join-message"])
        message = main.replace_member(message, member)
        await channel.send(message)
        if self.join_message["join-dm"] != "":
            dm = main.replace_relevant(self.join_message["join-dm"])
            dm = main.replace_member(dm, member).replace("%%server%%", member.guild.name)
            await member.send(dm)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(self.join_message["leave-channel"])
        message = main.replace_relevant(self.join_message["leave-message"])
        message = main.replace_member(message, member).replace("%%server%%", member.guild.name)
        await channel.send(message)


def setup(bot):
    bot.add_cog(JoinMessages(bot))
