import discord

client = discord.Client()

client.run(open("token.txt", "r").read())
