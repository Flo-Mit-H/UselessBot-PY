import mcrcon
from discord.ext import commands

import main


class Minecraft(commands.Cog):

    invalid_characters = ["§0", "§1", "§2", "§3", "§4", "§5", "§6", "§7", "§8", "§9", "§a", "§b", "§c", "§d", "§e", "§f"]

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        config = main.config["minecraft"]
        if not message.channel.id == config["console-channel"]:
            return
        if message.author.bot:
            return
        if message.content.startswith(config["prefix"]):
            command = message.content[len(config["prefix"]):]
            try:
                with mcrcon.MCRcon(host=config["server-host"], password=config["server-password"], port=config["server-port"]) as server:
                    server.connect()
                    feedback = server.command(command)
                    for char in self.invalid_characters:
                        feedback = feedback.replace(char, "")
                    if feedback == "" or feedback is None:
                        feedback = "Command ausgeführt"
                    await message.channel.send(f"```{feedback}```")
            except ConnectionRefusedError:
                await message.channel.send(f"Verbindung zum Server {config['server-host']}:{config['server-port']} fehlgeschlagen")


def setup(bot):
    bot.add_cog(Minecraft(bot))
