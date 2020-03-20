"""AI for generating responses for the chatbot"""

def get_bot_response(sender, message=None, attachments=None, entities=None):
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""

    if message:
        return "OMG!! You said '{}'".format(message)
    else:
        return "Come on, say something I can understand 🙄"