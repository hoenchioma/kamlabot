"""AI for generating responses for the chatbot"""

import random
import requests

CONFIDENCE_THRESHOLD = 0.7


def contains(text, cond):
    if isinstance(cond, list):
        return any(contains(text, i) for i in cond)
    elif isinstance(cond, tuple):
        return all(contains(text, i) for i in cond)
    elif isinstance(cond, str):
        return cond in text
    else:
        return False


def get_bot_response(sender, text=None, attachments=None, nlp=None):
    if (contains(text, (["tomorrow", "kalke", "kalk"], "class"))):
        return "No class tomorrow 😃"
    if (contains(text, ("csedu", ["site", "website"]))):
        return "https://sites.google.com/view/24csedu"
    if (contains(text, "syllabus")):
        return "Check the csedu24 site\nhttps://sites.google.com/view/24csedu"
    if (contains(text, "drive")):
        if (contains(text, "raheeb")):
            return "https://drive.google.com/open?id=1VskPt7flEiWEisDCNU9T7pfWTpVTa8PI"
        else:
            return "I think you'll find it here\nhttps://sites.google.com/view/24csedu/links?authuser=0"

    # others
    if (contains(text, (["tell", "bolo"], ["lame", "dad"], "joke"))):
        joke = requests.get('https://icanhazdadjoke.com/',
                            headers={'Accept': 'text/plain', }).text
        return joke

    # respond to general greeting
    entities = nlp['entities']
    if entities.get('thanks') and entities['thanks'][0]['confidence'] > CONFIDENCE_THRESHOLD:
        return "Your welcome 😃"
    if entities.get('greetings') and entities['greetings'][0]['confidence'] > CONFIDENCE_THRESHOLD:
        return random.choice(["Hi there", "Hello", "Hi"]) + random.choice([" 😃", ""])
    if entities.get('bye') and entities['bye'][0]['confidence'] > CONFIDENCE_THRESHOLD:
        return random.choice(["Ok, Bye", "Bye", "See you soon 😃"])

    return random.choice([
        "Error 404: not smart enough to respond to that",
        "Come on, say something I can understand 🙄",
        "Sorry, don't understand 😔",
        "😕",
        "Someday I'll be able to understand 🙂"
    ])
