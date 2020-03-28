"""AI for generating responses for the chatbot"""

import json
import random
import requests

CONFIDENCE_THRESHOLD = 0.7

HELP_MSG = """Hi I'm kamla bot, built for doing mostly kamlami :3
Try asking questions/statements like,
"kalke ki class?"
"csedu official site er link ki?"
"Give me Shamim's drive link"
"tell me a lame joke"
"Hi"
"Bye"

For now I can't understand Bangla characters, be sure to poke Raheeb until he implements it.
Peace out 😃

P.S: Stay safe and healthy everyone. Make sure to maintain social distancing and wash hands frequently
https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public"""


# load json data from info.json
with open("info.json", "r") as f:
    info = json.load(f)


def get_bot_response(sender, text=None, attachments=None, nlp=None):
    """Generate response based text, attachments and nlp entities"""

    if text:
        # show help/welcome message
        if (contains(text, "@help")):
            return HELP_MSG
        
        # classroom related
        if (contains(text, (["tomorrow", "kalke", "kalk"], "class"))):
            return "No class tomorrow 😃, stay indoors and wash your hands please"
        if (contains(text, ("csedu", ["site", "website"]))):
            if (contains(text, "24")):
                return f"CSEDU 24 batch website {info['site']['24']}"
            else:
                return f"CSEDU official site: {info['site']['csedu']}\nCSEDU 24 Batch website {info['site']['24']}"
        if (contains(text, "syllabus")):
            return f"Check the CSEDU 24 batch site\n{info['site']['24']}"
        if (contains(text, "drive")):
            for name in info['drive']['others']:
                if (contains(text, name)):
                    return f"{namify(name)}'s Google Drive folder link\n{info['drive']['others'][name]}"
            return f"You'll find all the drive links here\n{info['drive']['all']}"
        if (contains(text, ("google", "calendar"))):
            return f"CSEDU'24 classroom calendar: {info['calendar']['url']}\nYou can join here {info['calendar']['join']}"

        # others
        if (contains(text, "joke")):
            if (contains(text, ["lame", "dad"])):
                joke = requests.get('https://icanhazdadjoke.com/',
                                    headers={'Accept': 'text/plain', }).text
                return random.choice(["", "Ok here's a good one\n\n"]) + joke
            else:
                return "I only know lame jokes :3"

    if nlp:
        # respond to general greeting
        entities = nlp['entities']
        if entities.get('bye') and entities['bye'][0]['confidence'] > CONFIDENCE_THRESHOLD:
            return random.choice(["Ok, Bye", "Bye", "See you soon 😃"])
        if entities.get('thanks') and entities['thanks'][0]['confidence'] > CONFIDENCE_THRESHOLD:
            return "Your welcome 😃"
        if entities.get('greetings') and entities['greetings'][0]['confidence'] > CONFIDENCE_THRESHOLD:
            return random.choice(["Hi there", "Hello", "Hi"]) + random.choice([" 😃", ""])

    return random.choice([
        "Error 404: not smart enough to respond to that",
        "Come on, say something I can understand 🙄",
        "Sorry, don't understand 😔",
        "😕",
        "Someday I'll be able to understand 🙂"
    ])


def contains(text: str, cond) -> bool:
    """Recursive function to check if text contains
    a specific set of strings (following a set of rules)"""

    if isinstance(cond, list):  # list -> or logic
        return any(contains(text, i) for i in cond)
    elif isinstance(cond, tuple):  # tuple -> and logic
        return all(contains(text, i) for i in cond)
    elif isinstance(cond, str):
        return cond in text.lower()
    else:
        return False
    

def namify(name: str) -> str:
    """Captilize first letter of name"""
    return name[0].upper() + name[1:].lower()


if __name__ == "__main__":
    while True:
        print(get_bot_response("test_user", input()))
