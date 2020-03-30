import os
import logging
import discord

from .misc.ai import get_bot_response

TOKEN = os.environ['DISCORD_TOKEN']
KEYWORD = '!kamla'

# discord client (bot)
client = discord.Client()

# set logging level to info
logging.basicConfig(level=logging.INFO)


@client.event
async def on_ready():
    logging.info("[DISCORD] Discord bot server started ...")
    logging.info(
        f"[DISCORD] Logged in as [username: {str(client.user.name)}, id: {str(client.user.id)}]"
    )


@client.event
async def on_message(msg):
    channel = msg.channel

    # we do not want the bot to reply to itself
    if msg.author == client.user:
        return

    response = None

    # message starts with keyword
    if msg.content.startswith(KEYWORD):
        # remove the keyword prefix
        txt = msg.content[len(KEYWORD):]

        # replace other mentions with names
        txt = _replace_mentions(txt, msg.mentions)

        response = _process_msg(txt.strip(), msg.author)

    # bot is mentioned in message
    if client.user.mentioned_in(msg):
        txt = msg.content

        # remove mentions of the bot
        txt = txt.replace(f"<@{client.user.id}>", "")
        txt = txt.replace(f"<@!{client.user.id}>", "")

        # replace other mentions with names
        txt = _replace_mentions(txt, msg.mentions)

        response = _process_msg(txt.strip(), msg.author)

    if response:  # response isn't empty
        await channel.send(response)
        logging.info(f"[DISCORD] Response sent to {channel.name}")


def _process_msg(txt, author):
    """Process and return response for message"""
    response = get_bot_response(author.id, text=txt)
    # mention the user sending the message
    return author.mention + " " + response


def _replace_mentions(msg, mentions):
    """Convert mentions to corresponding names"""
    for member in mentions:
        msg = msg.replace(f"<@{member.id}>", member.name)
        msg = msg.replace(f"<@!{member.id}>", member.name)
    return msg


def main():
    client.run(TOKEN)


if __name__ == "__main__":
    main()
