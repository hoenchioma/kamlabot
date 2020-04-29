import json
import os
import re
from typing import Any

import pyrebase

config = json.loads(os.environ['FIREBASE_CONFIG'])

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def get_data(path: str) -> Any:
    """get data in specified path"""
    return db.child(path).get().val()


def get_responses(path: str = "") -> Any:
    """get an dict containing all app responses (corresponding to various message scenarios)"""
    return get_data('responses' + '/' + _process(path))


def get_info(path: str = "") -> Any:
    """get a dict containing all app info (links, calendar, etc.) """
    return get_data('info' + '/' + _process(path))


def get_others(path: str = "") -> Any:
    """get a dict containing other info (joke-api, etc)"""
    return get_data('others' + '/' + _process(path))


def _process(path: str) -> str:
    # remove leading "/" (if any) from path
    return re.sub('^/', '', path)


if __name__ == "__main__":
    print(json.dumps(get_data(''), indent=2))
