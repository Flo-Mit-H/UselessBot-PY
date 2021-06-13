import mcrcon
from discord.ext import commands

import main


class Minecraft(commands.Cog):

    invalid_characters = ["§0", "§1", "§2", "§3", "§4", "§5", "§6", "§7", "§8", "§9", "§a", "§b", "§c", "§d", "§e", "§f"]

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.channel.id == main.config["console-channel"]:
            return
        if message.author.bot:
            return
        if message.content.startswith(main.config["prefix"]):
            command = message.content[len(main.config["prefix"]):]
            with mcrcon.MCRcon(host=main.config["server-host"], password=main.config["server-password"], port=main.config["server-port"]) as server:
                server.connect()
                feedback = server.command(command)
                for char in self.invalid_characters:
                    feedback = feedback.replace(char, "")
                await message.channel.send(f"```{feedback}```")


def setup(bot):
    bot.add_cog(Minecraft(bot))
