import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

import main


class ReactionRoles(commands.Cog):
    reaction_roles = main.config["reaction-roles"]

    def __init__(self, bot):
        self.bot = bot

    async def process_reaction(self, payload: discord.RawReactionActionEvent, r_type=None):
        for reactrole in self.reaction_roles:
            if payload.message_id == reactrole["message-id"]:
                for obj in reactrole["roles"]:
                    if obj["emoji"] == payload.emoji.name:
                        guild = self.bot.get_guild(payload.guild_id)
                        user = await guild.fetch_member(payload.user_id)
                        role = guild.get_role(obj["role"])
                        if role is None:
                            print(f"An invalid Role ID {obj['role']} was provided in Reaction Roles for message {reactrole['message-id']}")
                        elif r_type == "add":
                            await user.add_roles(role)
                        elif r_type == "remove":
                            await user.remove_roles(role)
                        else:
                            print("Invalid Reaction Type was provided in reactroles.py `process_reaction`")
                            print("Not performing any Action as result")
                        break

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        await self.process_reaction(payload, "add")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        await self.process_reaction(payload, "remove")

    @commands.command()
    @has_permissions(manage_roles=True)
    async def reactrole(self, ctx, *, args):
        if not args:
            return
        args = args.split(" ")
        if ctx.message.reference is None:
            if len(args) < 3:
                return
            message_id = args[0]
            emoji = args[1]
            role_id = args[2]
        else:
            if len(args) < 2:
                return
            message_id = ctx.message.reference.message_id
            emoji = args[0]
            role_id = args[1]
        if ctx.message.role_mentions:
            role_id = ctx.message.role_mentions[0].id

        if message_id is None or emoji is None or role_id is None:
            await ctx.channel.send(main.replace_relevant(main.responses["reaction-role-command-invalid"]))
        if not (main.is_int(message_id) or main.is_int(role_id)):
            await ctx.channel.send(main.replace_relevant(main.responses["reaction-role-command-invalid"]))
            return
        message_id = int(message_id)
        role_id = int(role_id)
        for i in range(len(self.reaction_roles)):
            if self.reaction_roles[i]["message-id"] == message_id:
                main.config["reaction-roles"][i]["roles"].append({
                    "emoji": emoji,
                    "role": role_id
                })
                main.write_json("config.json", main.config)
                return
        main.config["reaction-roles"].append({
            "message-id": message_id,
            "roles": [
                {
                    "emoji": emoji,
                    "role": role_id
                }
            ]
        })
        main.write_json("config.json", main.config)
        message = await ctx.fetch_message(message_id)
        await message.add_reaction(emoji)
        await ctx.message.delete()
        await ctx.channel.send(main.responses["reaction-role-command-success"], delete_after=3)

    @reactrole.error
    async def reactrole_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await main.no_permission(ctx.message)


def setup(bot):
    bot.add_cog(ReactionRoles(bot))
