"""
Main module.
Tries to process updates.
If can't sends error to the chat or to the console,
in case of connection error or unavailability ot Telegram servers.
"""

from multiprocessing import Queue
from requests.exceptions import ConnectionError
from queue import Empty
from acr_bot.bot.objects import Update
from acr_bot.bot.exceptions import TelegramApiError, AcrCloudApiError


offset = None
q = Queue()


def process_updates(queue):
    """
    Attempts to recognize media provided by user.
    :param queue: Queue to pick update from.
    """
    while True:
        try:
            update = queue.get()
            upd = Update(update)
            usr_msg = upd.message
            chat = usr_msg.chat

            try:
                meta = usr_msg.media.recognize()
            except (AttributeError, ConnectionError, TelegramApiError) as e:
                if isinstance(e, AttributeError):
                    e = AttributeError('No media were provided.')
                send_error(chat, e)
            else:
                try:
                    usr_msg.media.get_music_meta(meta)
                except (AttributeError, AcrCloudApiError) as e:
                    send_error(chat, e)
                    if e != 'No result':
                        queue.put(update)

                chat.send_message(usr_msg.media.meta.get_info())
        except Empty:
            continue


def send_error(chat, e):
    """
    Sends error message to specified chat.
    :param chat: Chat to send error message.
    :param e: Error.
    """
    try:
        chat.send_message(e)
    except ConnectionError as e:
        print(e)
