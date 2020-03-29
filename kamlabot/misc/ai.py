"""AI for generating responses for the chatbot"""

import os
import json
import random
import requests
import logging

from . import database as db

# wit.ai
WIT_AI_TOKEN = os.environ['WIT_AI_CLIENT_TOKEN']

responses = db.get_responses()


def get_bot_response(sender, text=None, attachments=None):
    """Generate response based text, attachments and nlp entities"""
    try:
        if text:
            entities = get_entities(text)
            
            if ('@help' in text): return process(responses['help'])
            
                
            # detection using intent
            if (entities.get('intent')):
                intent = entities['intent'][0]['value']
                
                if (intent == 'help'): return process(responses['help'])
                if (intent == 'positive'): return process(responses['positive'])
                if (intent == 'negative'): return process(responses['negative'])
                if (intent == 'getBotIdentity'): return process(responses['identity'])
                
                # greetings (hi, bye, thanks)
                if (intent == 'greetings'): return process(responses['greetings'])
                if (intent == 'bye'): return process(responses['bye'])
                if (intent == 'thanks'): return process(responses['thanks'])
                
                # tasks
                if (intent == 'getSchedule'):
                    routine = db.get_info('routine')
                    gcal = db.get_info('google_calendar/url')
                    return f"The routine for 3-1 2020 is here {routine}\nYou can find an updated google calendar schedule here {gcal}"
                if (intent == 'getSiteLink'):
                    if (entities.get('website')):
                        return db.get_info('site/' + entities['website'][0]['value'])
                    else:
                        sites = db.get_info('site')
                        return '\n'.join([f"{site.upper()} site link: {link}" for site, link in sites.items()])
                if (intent == 'getSyllabus'):
                    syllabus = None
                    if entities.get('exam'):
                        syllabus = db.get_info('site/' + entities['exam'][0]['value'])
                        print()
                    else:
                        syllabus = db.get_info('site/_all')
                    return f"I think what you're looking for is here {syllabus}"
                if (intent == 'getDriveLink'):
                    drives = db.get_info('google_drive')
                    if entities.get('name') and entities['name'][0]['value'].lower() in drives:
                        name = entities['name'][0]['value']
                        link = drives[name.lower()]
                        return f"{name}'s drive folder link:\n{link}"
                    else:
                        return f"You'll find all the drive links here\n{drives['_all']}"
                if (intent == 'getJoke'):
                    return get_joke()
                
            # detection using other entities
            if (entities.get('greetings')): return process(responses['greetings'])
            if (entities.get('bye')): return process(responses['bye'])
            if (entities.get('thanks')): return process(responses['thanks'])
    
        # when bot doesn't understand the text
        return process(responses['no_reply'])
    
    except Exception as exp:
        logging.error(f"Error generating response ({str(exp)})")
        return None


def process(entry) -> str:
    """Process entries from database to generate responses"""
    try:
        if isinstance(entry, str): # if string return directly
            return entry
        elif isinstance(entry, list):
            if isinstance(entry[0], list): # if it is a list of lists
                # choose random string from each (internal) list and concatenate them
                return ''.join(random.choice(i) for i in entry)
            elif isinstance(entry[0], str): # if it is a list of strings
                # choose random string from list
                return random.choice(entry)
        raise "Incorrect type"
    except:
        logging.error("Incorrect formatting of data in database")
        return ""


def get_entities(msg: str) -> dict:
    """Get nlp entities using wit.ai"""
    WIT_AI_URL = 'https://api.wit.ai/message'
    headers = {'Authorization': 'Bearer ' + WIT_AI_TOKEN}
    params = (
        ('v', '20200328'),
        ('q', msg),
    )
    response = requests.get(WIT_AI_URL, headers=headers, params=params)
    return response.json()['entities']


def get_joke() -> str:
    """Get a joke randomly from one of 4/5 api choices"""
    choice = random.choices(
        ['lame', 'yo mama', 'chuck norris', 'programming', 'others'],
        weights=[3, 1, 0, 4, 4],  # weights
        k=1  # return only one answer
    )[0]
    if choice == 'lame':  # lame/dad jokes
        headers = {'Accept': 'application/json', }
        response = requests.get('https://icanhazdadjoke.com/', headers=headers)
        return response.json()['joke']
    elif choice == 'yo mama':  # yo mama jokes
        headers = {'Accept': 'application/json', }
        response = requests.get('https://api.yomomma.info/', headers=headers)
        return response.json()['joke']
    elif choice == 'chuck norris':  # Chuck Norris jokes
        headers = {'Accept': 'application/json', }
        response = requests.get(
            'http://api.icndb.com/jokes/random/', headers=headers)
        return response.json()['value']['joke']
    elif choice == 'programming':  # programming jokes
        response = requests.get(
            'https://sv443.net/jokeapi/v2/joke/Programming?blacklistFlags=nsfw&format=txt')
        return response.text
    else:  # other jokes
        response = requests.get(
            'https://sv443.net/jokeapi/v2/joke/Miscellaneous?blacklistFlags=nsfw&format=txt')
        return response.text


if __name__ == "__main__":
    while True:
        print(get_bot_response('00', text=input()))
