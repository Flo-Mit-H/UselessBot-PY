from datetime import datetime
import json
import os

import discord
import pytz
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

import main
from utils.message import no_permission


class Global(commands.Cog):
    if os.path.isfile("../config/global_servers.json"):
        with open("../config/global_servers.json", encoding="utf-8") as f:
            servers = json.load(f)
    else:
        servers = {"servers": []}
        with open("../config/global_servers.json", "w") as f:
            json.dump(servers, f, indent=4)

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["addGlobal"])
    @has_permissions(administrator=True)
    async def add_global(self, ctx):
        if not self.guild_exists(ctx.guild.id):
            server = {
                "guild-id": ctx.guild.id,
                "channel-id": ctx.channel.id,
                "invite": f"{(await ctx.channel.create_invite()).url}"
            }
            self.servers["servers"].append(server)
            with open("../config/global_servers.json", "w") as f:
                json.dump(self.servers, f, indent=4)
            embed = discord.Embed(title="**Willkommen beim GlobalChat!**", description="Dein Server ist nun zum Globalen Chat hinzugefügt worden!", color=0x2ecc71)
            embed.set_footer(text="Bitte beachte dass der GlobalChat-Channel normalerweise midestens 5 Sekunden Slow-Mode haben sollte.")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="Der GlobalChat existiert bereits.\r\n"
                                              "Jeder Server kann nur einen GlobalChat besitzen", color=0x2ecc71)
            await ctx.send(embed=embed)
        pass

    @add_global.error
    async def add_global_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await no_permission(ctx.message)

    @commands.command(aliases=["removeGlobal"])
    @has_permissions(administrator=True)
    async def remove_global(self, ctx):
        if self.guild_exists(ctx.guild.id):
            global_id = self.get_global_chat_id(ctx.guild.id)
            if global_id != -1:
                self.servers["servers"].pop(global_id)
                with open("../config/global_servers.json", "w") as f:
                    json.dump(self.servers, f, indent=4)
            embed = discord.Embed(title="**Auf wiedersehen!**",
                                  description=f"GlobalChat wurde entfernt. Du kannst ihn jederzeit mit `{main.config['prefix']}addGlobal` neu hinzufügen",
                                  color=0x2ecc71)
            await ctx.send(embed)
        else:
            embed = discord.Embed(description=f"Du hast noch keinen GlobalChat auf deinem Server! \r\n"
                                              f"Du kannst ihn jederzeit mit `{main.config['prefix']}addGlobal` neu hinzufügen",
                                  color=0x2ecc71)
            await ctx.send(embed)

    @remove_global.error
    async def remove_global_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await no_permission(ctx.message)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.content.startswith(main.config['prefix']):
            if self.get_global_chat(message.guild.id, message.channel.id):
                await self.send_all(message)
        await self.bot.process_commands(message)

    def guild_exists(self, guildid):
        for server in self.servers["servers"]:
            if int(server["guild-id"]) == int(guildid):
                return True
        return False

    def get_global_chat_id(self, guild_id):
        global_chat = -1
        i = 0
        for server in self.servers["servers"]:
            if int(server["guild-id"]) == int(guild_id):
                global_chat = i
            i += 1
        return global_chat

    async def send_all(self, message: discord.Message):
        content = message.content
        author = message.author
        attachments = message.attachments
        de = pytz.timezone("Europe/Berlin")
        embed = discord.Embed(description=content, timestamp=datetime.now().astimezone(tz=de), color=author.color)

        icon = author.avatar_url
        embed.set_author(name=author.name, icon_url=icon)

        icon_url = "https://i.redd.it/vf1qwxx3pqf51.jpg"
        icon = message.guild.icon_url
        if icon:
            icon_url = icon
        embed.set_thumbnail(url=icon_url)
        embed.set_footer(text=f"Gesendet von {message.guild.name}", icon_url=icon_url)

        links = f"[Glaube RDS]({main.config['storage']['rds-invite']}) ║ [Bot Einladung]({main.config['storage']['authorize']}) ║"
        global_chat = self.get_global_chat(message.guild.id, message.channel.id)
        if len(global_chat["invite"]) > 0:
            invite = global_chat["invite"]
            if "discord.gg" not in invite:
                invite = f"https://discord.gg/{invite}"
            links += f"[Server Invite]({invite}) ║"

        embed.add_field(name="Links & Hilfe", value=links, inline=False)

        if len(attachments) > 0:
            img = attachments[0]
            embed.set_image(url=img.url)

        for server in self.servers["servers"]:
            guild: discord.Guild = self.bot.get_guild(int(server["guild-id"]))
            if guild:
                channel: discord.TextChannel = guild.get_channel(int(server["channel-id"]))
                if channel:
                    perms: discord.Permissions = channel.permissions_for(guild.get_member(self.bot.user.id))
                    if perms.send_messages:
                        if perms.embed_links and perms.attach_files and perms.external_emojis:
                            await channel.send(embed=embed)
                        else:
                            await channel.send(f"{author.name}: {content}")
                            await channel.send("Mir Fehlen einige Rechte! Bitte gib mir Administrator-Rechte!")
        await message.delete()

    def get_global_chat(self, guild_id, channel_id=None):
        global_chat = None
        for server in self.servers["servers"]:
            if int(server["guild-id"]) == int(guild_id):
                if channel_id:
                    if int(server["channel-id"]) == int(channel_id):
                        global_chat = server
                else:
                    global_chat = server
        return global_chat


def setup(bot):
    bot.add_cog(Global(bot))
