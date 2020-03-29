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
    return get_data('responses' + '/' + path)

def get_info(path: str = "") -> OrderedDict:
    """get a dict containing all app info (links, calendar, etc.) """
    return get_data('info' + '/' + path)


if __name__ == "__main__":
    pass

