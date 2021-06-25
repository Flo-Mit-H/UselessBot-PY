from discord.ext import commands

import main
from utils.string import replace_relevant, replace_member
from utils.message import send_json


class JoinMessages(commands.Cog):
    join_message = main.config["join-message"]

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(self.join_message["join-channel"])
        message = replace_relevant(self.join_message["join-message"], member.guild)
        message = replace_member(message, member)
        await send_json(channel=channel, json_data=self.join_message["join-message"], msg=message)
        if self.join_message["join-dm"] != "":
            dm = replace_relevant(self.join_message["join-dm"], member.guild)
            dm = replace_member(dm, member).replace("%%server%%", member.guild.name)
            await send_json(channel=member, json_data=self.join_message["join-dm"], msg=dm)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(self.join_message["leave-channel"])
        message = replace_relevant(self.join_message["leave-message"], member.guild)
        message = replace_member(message, member).replace("%%server%%", member.guild.name)
        await send_json(channel, self.join_message["leave-message"], msg=message)


def setup(bot):
    bot.add_cog(JoinMessages(bot))
