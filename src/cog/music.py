import asyncio

import youtube_dl
from discord.ext import commands

from utils.message import *
import main

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, executable=main.config["ffmpeg-path"], **ffmpeg_options), data=data)


class Music(commands.Cog):

    def __init(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *args):

        """Joins a voice channel"""
        if ctx.author.voice is not None:
            channel = ctx.author.voice.channel
        else:
            if len(args) > 0:
                channel = discord.utils.get(ctx.guild.channels, name=args[0])
            else:
                return await ctx.message.add_reaction("❌")

        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()

        await ctx.message.add_reaction("👍")

    @commands.command()
    async def play(self, ctx, *, url):

        """Streams from a url (same as yt, but doesn’t predownload"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        await send_json(ctx.channel, main.responses["now-playing"], msg=replace_relevant(main.responses["now-playing"]["content"]
                                                                                                      .replace("%%title%%", player.title), ctx.guild))

    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await send_usage(ctx, "play")

    @commands.command()
    async def yt(self, ctx, *, url):

        """Plays from a url (almost anything youtube_dl supports"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        await send_json(ctx.channel, main.responses["not-playing"], msg=replace_relevant(main.responses["now-playing"]["content"]
                                                                                                      .replace("%%title%%", player.title), ctx.guild))

    @yt.error
    async def yt_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await send_usage(ctx, "yt")

    @commands.command()
    async def volume(self, ctx, volume: int):

        """Changes the Player´s Volume"""

        if ctx.voice_client is None:
            return await ctx.message.add_reaction("❌")

        ctx.voice_client.source.volume = volume / 100
        await send_json(ctx.channel, main.responses["changed-volume"], msg=main.responses["changed-volume"]["content"]
                                     .replace("%%volume%%", str(volume)))

    @volume.error
    async def volume_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await send_usage(ctx, "volume")

    @commands.command()
    async def stop(self, ctx):
        """Stops the bot"""
        ctx.voice_client.stop()
        await ctx.message.add_reaction("👍")

    @commands.command(aliases=["disconnect"])
    async def leave(self, ctx):
        voice = ctx.voice_client
        if voice is not None:
            await voice.disconnect()
            await ctx.message.add_reaction("👍")
        else:
            await send_json(ctx.channel, main.responses["not-connected"], msg=replace_relevant(main.responses["not-connected"]["content"], ctx.guild))
            await ctx.message.add_reaction("❌")

    @commands.command()
    async def pause(self, ctx):
        """Pauses the bot"""
        voice = ctx.voice_client
        if voice.is_playing():
            voice.pause()
            await ctx.message.add_reaction("👍")
        else:
            await ctx.message.add_reaction("❌")

    @commands.command()
    async def resume(self, ctx):
        """Resumes the Bot"""
        voice = ctx.voice_client
        if voice.is_paused():
            voice.resume()
            await ctx.message.add_reaction("👍")
        else:
            await ctx.message.add_reaction("❌")

    @play.before_invoke
    @yt.before_invoke
    async def ensure_voice(self, ctx):
        """Makes sure the bot can play music"""
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await send_json(ctx.channel, main.responses["not-in-vc"])
                raise commands.CommandError("Author not connected to a voice channel")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def setup(bot):
    bot.add_cog(Music(bot))
