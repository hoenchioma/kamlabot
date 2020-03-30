import os
import logging
from flask import Flask, request
from pymessenger.bot import Bot

from .misc.ai import get_bot_response

# set config variables
ACCESS_TOKEN = os.environ['FB_ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['FB_VERIFY_TOKEN']

app = Flask(__name__)
bot = Bot(ACCESS_TOKEN)

# set logging level to info
logging.basicConfig(level=logging.INFO)


@app.route('/')
def hello():
    """Greet use who visits the actual url"""
    return "Hello! 😃"


@app.route('/webhook', methods=['GET', 'POST'])
def listen():
    """This is the main function flask uses to 
    listen at the `/webhook` endpoint"""

    # process verification request (verify that the request came from Facebook)
    if request.method == 'GET':
        return _verify_webhook(request)

    # responding to a message
    if request.method == 'POST':
        payload = request.json
        # logging.info("message: " + repr(payload))
        for event in payload['entry']:
            for messaging in event['messaging']:
                if (messaging.get('message') and
                        not messaging['message'].get('is_echo')):
                    sender_id = messaging['sender']['id']
                    message = messaging['message']

                    # extract contents of message
                    text = message.get('text')
                    attachments = message.get('attachments')

                    # if text or attachments (image/gif) is present
                    if text or attachments:
                        # respond to message
                        _respond(sender_id, text, attachments)
        return "ok"


def _verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"


def _send_message(recipient_id, text):
    """Send a response to Facebook"""

    bot.send_text_message(recipient_id, text)
    return "success"


def _respond(sender, text=None, attachments=None):
    """Formulate a response to the user and
    pass it on to a function that sends it."""

    response = get_bot_response(sender, text, attachments)
    if response:
        _send_message(sender, response)


def main():
    # run the server
    app.run()


if __name__ == '__main__':
    main()
