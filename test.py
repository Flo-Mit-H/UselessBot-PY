import requests
from discord.ext import commands

import main


class Test(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def __discord_get(url, params=None, payload=None, session=None):
        request_headers = {"Authorization", f"Bot {main.token}"}
        session = requests.Session() if session is None else session

        session.get(f"https://discord.com/api/v9/{url}", params=params)

    @staticmethod
    def __discord_post():
        pass

    @commands.command()
    async def test(self, ctx):
        # name = self.bot.user.name
        # avatar = self.bot.user.avatar
        # json = main.config["test"]

        # # Get Webhook
        # webhooks = await ctx.channel.webhooks()
        # if webhooks:
        #     webhook = webhooks[0]
        # else:
        #     webhook = await ctx.channel.create_webhook(name=name, avatar=avatar)

        # # Do some Avatar and JSON stuff
        # if not json["username"]:
        #     json["username"] = self.bot.user.name
        # try:
        #     temp = json["avatar"]
        # except KeyError:
        #     request_headers = {
        #         "Authorization": f"Bot {open('token.txt', 'r').read()}"
        #     }
        #     userjson = requests.get("https://discord.com/api/v9/users/@me", headers=request_headers).json()
        #     print(userjson)
        #     json["avatar"] = userjson["avatar"]

        # # Send Data to Webhook URL
        # result = requests.post(webhook.url, json=json)
        # try:
        #     result.raise_for_status()
        # except requests.exceptions.HTTPError as err:
        #     print(err)
        # else:
        #     print(f'Payload delivered successfully! Code: \n{json}\nResult: {result.text}')

        pass


def setup(bot):
    bot.add_cog(Test(bot))
