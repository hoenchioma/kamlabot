"""AI for generating responses for the chatbot"""

import os
import json
import random
import requests
import logging
from dpath.util import get
from typing import List, Union

from . import database as db
from .. import __version__

# wit.ai
WIT_AI_URL = 'https://api.wit.ai/message'
WIT_AI_TOKEN = os.environ['WIT_AI_CLIENT_TOKEN']


def get_bot_response(sender, text=None, attachments=None) -> str:
    """Generate response based text, attachments and nlp entities"""
    try:
        if text:
            entities = _get_entities(text)

            if ('@help' in text):
                return _get_help_txt()

            # detection using intent
            if (entities.get('intent')):
                intent = entities['intent'][0]['value']

                if (intent == 'help'):
                    return _get_help_txt()
                if (intent == 'positive'):
                    return _process(_get_responses('positive'))
                if (intent == 'negative'):
                    return _process(_get_responses('negative'))
                if (intent == 'getBotIdentity'):
                    return _process(_get_responses('identity'))

                # greetings (hi, bye, thanks)
                if (intent == 'greetings'):
                    return _process(_get_responses('greetings'))
                if (intent == 'bye'):
                    return _process(_get_responses('bye'))
                if (intent == 'thanks'):
                    return _process(_get_responses('thanks'))

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
                        return '\n'.join(f"{site.upper()} site link: {link}" for site, link in sites.items())
                if (intent == 'getSyllabus'):
                    syllabus = None
                    if entities.get('exam'):
                        syllabus = db.get_info(
                            'site/' + entities['exam'][0]['value'])
                    else:
                        syllabus = db.get_info('site/__all__')
                    return f"I think what you're looking for is here {syllabus}"
                if (intent == 'getDriveLink'):
                    drives = db.get_info('google_drive')
                    if entities.get('name') and entities['name'][0]['value'].lower() in drives:
                        name = entities['name'][0]['value']
                        link = drives[name.lower()]
                        return f"{name}'s drive folder link:\n{link}"
                    else:
                        return f"You'll find all the drive links here\n{drives['__all__']}"
                if (intent == 'getJoke'):
                    return _get_joke()

            # detection using other entities
            if (entities.get('greetings')):
                return _process(_get_responses('greetings'))
            if (entities.get('bye')):
                return _process(_get_responses('bye'))
            if (entities.get('thanks')):
                return _process(_get_responses('thanks'))

        # when bot doesn't understand the text
        return _process(_get_responses('no_reply'))

    except Exception as exp:
        logging.error(f"Error generating response ({str(exp)})")
        return None


def _process(entry: Union[str, List[str], List[List[str]]]) -> str:
    """Process entries from database to generate responses"""
    try:
        if isinstance(entry, str):  # if string return directly
            return entry
        elif isinstance(entry, list):
            if isinstance(entry[0], list):  # if it is a list of lists
                # choose random string from each (internal) list and concatenate them
                return ''.join(random.choice(i) for i in entry)
            elif isinstance(entry[0], str):  # if it is a list of strings
                # choose random string from list
                return random.choice(entry)
        raise "Incorrect type"
    except:
        logging.error("Incorrect formatting of data in database")
        return ""


def _get_responses(key: str) -> Union[str, List[str], List[List[str]]]:
    """Get responses from db according to key"""
    try:
        # return cached result
        return _get_responses.cache[key]
    except AttributeError:
        # if responses not cached save db response to cache
        _get_responses.cache = db.get_responses()
        return _get_responses.cache[key]


def _get_entities(msg: str) -> dict:
    """Get nlp entities using wit.ai"""
    headers = {'Authorization': 'Bearer ' + WIT_AI_TOKEN}
    params = (('v', '20200328'), ('q', msg),)
    response = requests.get(WIT_AI_URL, headers=headers, params=params)
    return response.json()['entities']


def _get_joke() -> str:
    """Get a joke randomly from one of several api choices"""
    api_list = db.get_others('joke-api/__list__')
    # randomly choose a single api
    api_key = random.choices(
        [api['key'] for api in api_list],
        weights=[api['weight'] for api in api_list],  # weights
        k=1  # return only one answer
    )[0]
    logging.info(f"Using joke api \"{api_key}\"")

    api = db.get_others('joke-api/' + api_key)

    response = requests.get(api['url'], headers=api.get('headers'))
    if api['result']['type'] == "json":
        return get(response.json(), api['result']['path'])
    elif api['result']['type'] == "text":
        return response.text


def _get_help_txt() -> str:
    """Return help text with the version number of the app"""
    return _process(_get_responses('help')) + f"\n\n(kamlabot v{__version__})"


if __name__ == "__main__":
    while True:
        print(get_bot_response('00', text=input()))
