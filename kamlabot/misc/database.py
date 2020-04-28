import os
import pyrebase
import json

from collections import OrderedDict

config = json.loads(os.environ['FIREBASE_CONFIG'])

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def get_data(path: str) -> OrderedDict:
    """ get data in specified path (in the form of an OrderedDict) """
    return db.child(path).get().val()

def get_responses(path: str = "") -> OrderedDict:
    """get an dict containing all app responses (corresponding to various message scenarious)"""
    # remove any leading slashes
    if len(path) >= 1 and path[0] == '/':
        path = path[1:]
    return get_data('responses' + '/' + path)

def get_info(path: str = "") -> OrderedDict:
    """get a dict containing all app info (links, calendar, etc.) """
    # remove any leading slashes
    if len(path) >= 1 and path[0] == '/':
        path = path[1:]
    return get_data('info' + '/' + path)

def get_others(path: str = "") -> OrderedDict:
    """get a dict containing other info (joke-api, etc)"""
    # remove any leading slashes
    if len(path) >= 1 and path[0] == '/':
        path = path[1:]
    return get_data('others' + '/' + path)


if __name__ == "__main__":
    print(json.dumps(get_data(''), indent=2))

