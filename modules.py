from discord.ext import commands

import main


class Modules(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["load-module", "load_extension", "load-extension"])
    async def load_module(self, ctx, module):
        main.client.load_extension(module)
        await ctx.channel.send(main.replace_relevant(main.responses["load-extension-success"]).replace("%%extension%%", module))

    @commands.command(aliases=["unload-module", "unload_extension", "unload-extension"])
    async def unload_module(self, ctx, module):
        main.client.unload_extension(module)
        await ctx.channel.send(main.replace_relevant(main.responses["unload-extension-success"]).replace("%%extension%%", module))

    @commands.command(aliases=["list-modules", "list_extensions", "list-extensions"])
    async def list_modules(self, ctx):
        extensions = list(self.bot.extensions.keys())
        message = ""
        for extension in extensions:
            message += f"{extension}\n"
        await ctx.channel.send(message)

    @commands.command(aliases=["reload-module", "reload_extension", "reload-extension"])
    async def reload_module(self, ctx, module):
        main.client.reload_extension(module)
        await ctx.channel.send(main.replace_relevant(main.responses["reload-extension-success"]).replace("%%extension%%", module))

    @commands.command(aliases=["reload-modules", "reload_extensions", "reload-extensions"])
    async def reload_modules(self, ctx):
        extensions = list(self.bot.extensions.keys())
        for extension in extensions:
            await self.reload_module(ctx, extension)


def setup(bot):
    bot.add_cog(Modules(bot))
