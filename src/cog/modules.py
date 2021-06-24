from discord.ext import commands

from utils.message import *
import main


class Modules(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["load-module", "load_extension", "load-extension"])
    async def load_module(self, ctx, module):
        main.bot.load_extension(module)
        await main.message.send_json(ctx.channel, main.responses["load-extension-success"], msg=replace_relevant(main.responses["load-extension-success"]["content"], ctx.guild)
                                     .replace("%%extension%%", module))

    @load_module.error
    async def load_module_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await send_usage(ctx, "load-module")

    @commands.command(aliases=["unload-module", "unload_extension", "unload-extension"])
    async def unload_module(self, ctx, module):
        main.bot.unload_extension(module)
        await main.message.send_json(ctx.channel, main.responses["unload-extension-success"], msg=replace_relevant(main.responses["unload-extension-success"]["content"], ctx.guild)
                                     .replace("%%extension%%", module))

    @unload_module.error
    async def unload_module_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await send_usage(ctx, "unload-module")

    @commands.command(aliases=["list-modules", "list_extensions", "list-extensions"])
    async def list_modules(self, ctx):
        extensions = list(self.bot.extensions.keys())
        message = ""
        for extension in extensions:
            message += f"{extension}\n"
        await ctx.channel.send(message)

    @commands.command(aliases=["reload-module", "reload_extension", "reload-extension"])
    async def reload_module(self, ctx, module):
        main.bot.reload_extension(module)
        await main.message.send_json(ctx.channel, main.responses["reload-extension-success"], msg=replace_relevant(main.responses["reload-extension-success"]["content"], ctx.guild)
                                     .replace("%%extension%%", module))

    @reload_module.error
    async def reload_module_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await send_usage(ctx, "reload-module")

    @commands.command(aliases=["reload-modules", "reload_extensions", "reload-extensions"])
    async def reload_modules(self, ctx):
        extensions = list(self.bot.extensions.keys())
        for extension in extensions:
            await self.reload_module(ctx, extension)


def setup(bot):
    bot.add_cog(Modules(bot))
