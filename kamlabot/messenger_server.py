import logging
import os

from flask import Flask, request, redirect
from pymessenger.bot import Bot

from .misc import ai
from . import VERBOSE

GITHUB_URL = 'https://github.com/hoenchioma/kamlabot'

# set config variables
ACCESS_TOKEN = os.environ['FB_ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['FB_VERIFY_TOKEN']

# setup logger
logging.basicConfig(level=logging.INFO,
                    format='[MESSENGER] %(levelname)s : %(module)s.%(funcName)s : %(message)s')

# initialize app
app = Flask(__name__)
bot = Bot(ACCESS_TOKEN)

WOKE = False

@app.route('/')
def hello():
    global WOKE
    text = f'Hello there 😄, this the landing page of kamlabot.<br>It\'s pretty empty right now.<br>You can go here <a href="{GITHUB_URL}">here</a> to see the GitHub page.'
    if not WOKE:
        WOKE = True
        return "Was sleep, am woke now 😴. The discord bot should work now" + "<br><br>" + text
    else:
        return text 


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

    logging.info(f"Response sent to {recipient_id}")
    return "success"


def _respond(sender, text=None, attachments=None):
    """Formulate a response to the user and
    pass it on to a function that sends it."""

    try:
        response = ai.get_bot_response(sender, text, attachments)
        try:
            _send_message(sender, response)

            # log event
            if VERBOSE:
                logging.info("Response successfully sent\n"
                             f"sender: {sender}\n"
                             f"message: {text}\n"
                             f"response: {response}")
            else:
                logging.info(f"Response sent successfully to {sender}")
        except:
            logging.exception("Error sending generated response to Facebook")
    except:
        logging.exception("Error generating response")


def main():
    # run the server
    app.run()


if __name__ == '__main__':
    main()
