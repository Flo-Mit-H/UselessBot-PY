import asyncio
import logging

import discord
from discord.ext import commands

from utils.configuration import config

# define nescessary variables
bot = commands.Bot(command_prefix=config["prefix"], intents=discord.Intents.all())

responses = config["responses"]
usages = config["usages"]


class Application:
    """
    This class is the main application of the Aqua bot.
    When started, it blocks the main thread and runs the bot.
    """

    # Cogs to activate at startup
    __cogs = [
        "clear",
        "join_messages",
        "join_roles",
        "level",
        "minecraft",
        "mod",
        "modules",
        "music",
        "ping",
        "prefix",
        "reactroles",
        "stop"
    ]

    def __init__(self, discord_bot, bot_token):
        # Bot Create Logic
        self.bot = discord_bot
        self.logger = logging.getLogger("main")
        self.logger.setLevel(logging.DEBUG if config["debug"] else logging.INFO)

        self.load_extensions()

        @self.bot.event
        async def on_ready():
            # Bot statup logic
            self.logger.info(f"Logged in as {self.bot.user.name}#{self.bot.user.discriminator}")
            self.logger.debug("Initializing Update Task")
            bot.loop.create_task(self.update_task())
            self.logger.info("Initialized Update Task")

        # Run aqua
        self.bot.run(bot_token)

    def load_extensions(self):
        for extension in self.__cogs:
            self.logger.debug(f"Loading Extension {extension}")

            __import__(f"cog.{extension}", fromlist=["setup"]).setup(bot)

            self.logger.info(f"Loaded Extension {extension}")
        self.logger.info(f"Loaded {len(self.__cogs)} Extensions in total")

    @staticmethod
    async def update_task():
        while True:
            for state in config["rich-presence"]["states"]:
                # Prefix
                bot.command_prefix = config["prefix"]

                # Activity
                activity = discord.Game(state["message"])

                # Status
                statusstr = state["status"]
                status = discord.Status.online
                if statusstr == "idle":
                    status = discord.Status.idle
                elif statusstr == "dnd" or statusstr == "do_not_disturb":
                    status = discord.Status.do_not_disturb
                elif statusstr == "offline" or statusstr == "Offline":
                    status = discord.Status.offline

                await bot.change_presence(activity=activity, status=status, afk=state["afk"])
                await asyncio.sleep(config["rich-presence"]["delay"])


# discord log config
logging.basicConfig(
    level=logging.DEBUG if config["debug"] else logging.INFO,
    format='(%(asctime)s) %(levelname)7s - %(name)20s: %(message)s'
)

# Read token from file
token = open("../config/token.txt", "r").read()

if __name__ == '__main__':
    Application(bot, token)
