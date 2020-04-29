import logging
import os
from typing import List, Union

import discord

from .misc import ai
from . import VERBOSE

TOKEN = os.environ['DISCORD_TOKEN']
KEYWORD = '!kamla'

# discord client (bot)
client = discord.Client()

# setup logger
logging.basicConfig(level=logging.INFO,
                    format='[DISCORD] %(levelname)s : %(module)s.%(funcName)s : %(message)s')


@client.event
async def on_ready():
    logging.info("Discord bot server started ...")
    logging.info(
        f"Logged in as [username: {str(client.user.name)}, id: {str(client.user.id)}]"
    )


@client.event
async def on_message(msg: discord.Message):
    """Called on receiving a message"""
    channel = msg.channel

    # we do not want the bot to reply to itself
    if msg.author == client.user:
        return

    # if message is in DM channel, starts with keyword
    # or bot is mentioned in msg
    if isinstance(channel, discord.DMChannel) \
            or msg.content.startswith(KEYWORD) \
            or client.user.mentioned_in(msg):
        if msg.content.startswith(KEYWORD):
            txt = msg.content[len(KEYWORD):]  # remove keyword from msg
        else:
            txt = msg.content

        txt = _remove_bot_mentions(txt)
        txt = _replace_mentions_with_names(txt, msg.mentions)

        try:
            response = ai.get_bot_response(msg.author.id, txt.strip())
            try:
                # if it is not a DM channel mention recipient
                if not isinstance(channel, discord.DMChannel):
                    response = msg.author.mention + " " + response
                await channel.send(response)

                # log the event
                if VERBOSE:
                    logging.info("Response successfully sent\n"
                                 f"sender: [name: {msg.author.name}, id: {msg.author.id}]\n"
                                 f"channel: {_get_channel_identifier(channel)}\n"
                                 f"message: {txt}\n"
                                 f"response: {response}")
                else:
                    logging.info("Response sent successfully to "
                                 f"{msg.author.name} in {_get_channel_identifier(channel)}")
            except:
                logging.exception("Error sending generated response to Discord")
        except:
            logging.exception("Error generating response")


def _remove_bot_mentions(txt: str) -> str:
    """Remove mentions of the bot"""
    txt = txt.replace(f"<@{client.user.id}>", "")
    txt = txt.replace(f"<@!{client.user.id}>", "")
    return txt


def _replace_mentions_with_names(
        txt: str,
        mentions: List[Union[discord.User,
                             discord.Member]]) -> str:
    """Convert mentions to corresponding names"""
    for member in mentions:
        txt = txt.replace(f"<@{member.id}>", member.name)
        txt = txt.replace(f"<@!{member.id}>", member.name)
    return txt


def _get_channel_identifier(
        channel: Union[discord.TextChannel,
                       discord.DMChannel,
                       discord.GroupChannel]) -> str:
    """Get channel identifier based on the type of channel it is"""
    if isinstance(channel, discord.TextChannel):
        return f"[server: {channel.guild.name}, channel: {channel.name}, id: {channel.id}]"
    elif isinstance(channel, discord.DMChannel):
        return f"[user: {channel.recipient.name}, id: {channel.id}]"
    elif isinstance(channel, discord.GroupChannel):
        members = ','.join(user.name for user in channel.recipients)
        return f"[group: {channel.name}, members: ({members}), id: {channel.id}]"


def main():
    client.run(TOKEN)


if __name__ == "__main__":
    main()
