import logging
from flask import Flask, request
from pymessenger.bot import Bot
from ai import get_bot_response
from credentials import *


app = Flask(__name__)
bot = Bot(ACCESS_TOKEN)

# set logging level to debug
logging.basicConfig(level=logging.DEBUG)


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
        return verify_webhook(request)

    # responding to a message
    if request.method == 'POST':
        payload = request.json
        logging.info("message:\n" + repr(payload))
        for event in payload['entry']:
            for message in event['messaging']:
                if (message.get('message') and
                        not message['message'].get('is_echo')):
                    # get the facebook messenger ID of sender
                    sender_id = message['sender']['id']
                    text = message['message'].get('text')
                    attachments = message['message'].get('attachments')
                    # if text or attachments (image/gif) is present
                    if text or attachments:
                        # respond to message
                        respond(sender_id, text, attachments)
        return "ok"


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"


def send_message(recipient_id, text):
    """Send a response to Facebook"""

    bot.send_text_message(recipient_id, text)
    return "success"


def respond(sender, message=None, attachments=None, entities=None):
    """Formulate a response to the user and
    pass it on to a function that sends it."""

    response = get_bot_response(sender, message, attachments, entities)
    if response:
        send_message(sender, response)


# run the server
if __name__ == '__main__':
    app.run()
