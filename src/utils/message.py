import discord
import requests

from main import responses, usages, token
from utils.string import replace_relevant


async def no_permission(message: discord.Message):
    await message.reply(replace_relevant(responses["no-permission"], message.channel.guild))


async def send_usage(ctx, name):
    await send_json(ctx, replace_relevant(usages[f"{name}-usage"], ctx.guild))


class HttpCodeErrors:
    class NoPermission(Exception):
        pass

    class ServerError(Exception):
        pass

    class NotFound(Exception):
        pass

    class Other(Exception):
        def __init__(self, code):
            self.code = code


def handle_code(responsecode):
    if responsecode < 300:
        return
    elif responsecode == 403:
        raise HttpCodeErrors.NoPermission()
    elif responsecode == 500:
        raise HttpCodeErrors.ServerError()
    elif responsecode == 404:
        raise HttpCodeErrors.NotFound()
    else:
        raise HttpCodeErrors.Other(responsecode)


def discord_get(url, params=None, session=None):
    request_headers = {"Authorization", f"Bot {token}"}
    session = requests.Session() if session is None else session

    response = session.get(f"https://discord.com/api/v9/{url}", params=params, headers=request_headers)
    handle_code(response.status_code)
    return response.json()


def discord_post(url, params=None, session=None):
    request_headers = {"Authorization", f"Bot {token}"}
    session = requests.Session() if session is None else session

    response = session.post(f"https://discord.com/api/v9/{url}", params=params, headers=request_headers)
    handle_code(response.status_code)
    return response.json()


async def send_json(channel, json_data, *, tts=False, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None, msg=None):
    if str(json_data) == json_data:
        msg = json_data
    else:
        if msg is None:
            msg = json_data["content"]
    embed = None
    try:
        embed = discord.Embed.from_dict(json_data["embed"])
    except KeyError:
        pass

    return await channel.send(content=msg, embed=embed, tts=tts, file=file, files=files, delete_after=delete_after, nonce=nonce, allowed_mentions=allowed_mentions,
                              reference=reference, mention_author=mention_author)
