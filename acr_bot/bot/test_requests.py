"""
This module can be used for testing webhook.
It allows to specify JSON data and make requests to provided url.
"""

import requests

from multiprocessing import Pool, current_process
from requests.exceptions import ConnectionError
from json import dumps
from acr_bot.config import url_wh


def send_post(body):
    """
    Sends posts request with provided JSON.
    :param body: Request body data.
    :return: Response.
    """
    response = None
    print('Sending request...')
    try:
        response = requests.post(url_wh, data=dumps(body))
    except ConnectionError as error:
        print(current_process().name, error)
    print(response)
    return response


def repeat_sequence(seq, times=2):
    """
    Repeat given sequence n times.
    :param seq: Sequence to repeat.
    :param times: Number of times. By default = 2.
    :return: Larger sequence consists of given sequence repeated n times.
    """
    return seq * times


def handle(iterations=1):
    """
    Creates pool of workers to send requests.
    :param iterations: Number of iterations through data.
    """
    p = Pool()
    d = repeat_sequence(data, iterations)
    result = p.map(send_post, d)
    print(result)


data = ({
    "update_id": "881492748",
    "message": {
        "message_id": "382",
        "from": {
            "id": "63507262",
            "is_bot": "False",
            "first_name": "Denis",
            "last_name": "Ivanov",
            "username": "Ledorub",
            "language_code": "en"
        },
        "chat": {
            "id": "63507262",
            "first_name": "Denis",
            "last_name": "Ivanov",
            "username": "Ledorub",
            "type": "private"
        },
        "date": "1555250808",
        "audio": {
            "duration": "216",
            "mime_type": "audio/mp3",
            "title": "Jinco-Tokyo",
            "performer": "ДАБСТЕП(DubStep)",
            "file_id": "CQADAgADFgQAAgaM0UhOOcd2kp29qQI",
            "file_size": "8703874"
        }
    }
}, {
    "update_id": "881492749",
    "message": {
        "message_id": "383",
        "from": {
            "id": "63507262",
            "is_bot": "False",
            "first_name": "Denis",
            "last_name": "Ivanov",
            "username": "Ledorub",
            "language_code": "en"
        },
        "chat": {
            "id": "63507262",
            "first_name": "Denis",
            "last_name": "Ivanov",
            "username": "Ledorub",
            "type": "private"
        },
        "date": "1555250808",
        "audio": {
            "duration": "176",
            "mime_type": "audio/mp3",
            "title": "Lost",
            "performer": "Vosai",
            "file_id": "CQADAgADLAQAAp_g2UirJZtNlzfS5QI",
            "file_size": "7132935"
        }
    }
}, {
    "update_id": "881492720",
    "message": {
        "message_id": "327",
        "from": {
            "id": "63507262",
            "is_bot": "False",
            "first_name": "Denis",
            "last_name": "Ivanov",
            "username": "Ledorub",
            "language_code": "en"
        },
        "chat": {
            "id": "63507262",
            "first_name": "Denis",
            "last_name": "Ivanov",
            "username": "Ledorub",
            "type": "private"
        },
        "date": "1555250808",
        "audio": {
            "duration": "234",
            "mime_type": "audio/mp3",
            "title": "Recovery",
            "performer": "LP",
            "file_id": "CQADAgADLgQAAp_g2UiksA3j15OLUAI",
            "file_size": "9532067"
        }
    }
})


if __name__ == '__main__':
    iterations = 1
    handle(iterations)
