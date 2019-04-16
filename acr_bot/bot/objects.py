"""
Provide classes to work with update and other objects contained in it.
User message object and media objects that can be recognized by ACRCloud API.
Also contains some methods to get and parse these media objects.
"""

import requests
import acr_bot.bot.exceptions as exceptions

from json import loads
from datetime import date
from string import Template
from acr_bot.config import url, url_file, proxies
from acr_bot.bot.recognizer import get_recognizer


class Update:
    """
    Represents an update object received from Telegram API.
    """

    def __init__(self, upd):
        self.id = upd.get('update_id')
        self.message = Message(upd.get('message')) if upd.get('message') else None


class Message:
    """
    Represents a message object that is contained in an update object.
    """

    def __init__(self, msg):
        """
        :param msg: Message object from Telegram API.
        """
        self.message_id = msg.get('message_id')
        self.from_ = User(msg.get('from'))
        self.date = msg.get('date')
        self.chat = Chat(msg.get('chat'))
        self.media = None
        self.entities = Entities(msg.get('entities')) if msg.get('entities') else None

        self.get_media(msg)

    def get_media(self, msg):
        """
        Determines type of an object sent by user
        and creates instance of the right type.
        :param msg: Message object from Telegram API.
        """
        media = ((Audio, 'audio'), (Video, 'video'),
                 (Voice, 'voice'), (VideoNote, 'video_note'))

        for type_, obj_name in media:
            try:
                obj = msg.get(obj_name)
                self.media = type_(obj)
            except AttributeError:
                continue


class User:
    """
    Represents a user object that is contained in an update object.
    """

    def __init__(self, usr):
        """
        :param usr: User object from Telegram API.
        """
        self.id = usr.get('id')
        self.is_bot = usr.get('is_bot')
        self.first_name = usr.get('first_name')
        self.language_code = usr.get('language_code')


class Chat:
    """
    Represents a chat object that is contained in an update object.
    """

    def __init__(self, chat):
        """
        :param chat: Chat object from Telegram API.
        """
        self.id = chat.get('id')
        self.type = chat.get('type')
        self.title = chat.get('title')
        self.username = chat.get('username')

    def send_message(self, text):
        """
        Sends message with provided text to the chat.
        :param text: Text to send.
        """
        params = {'chat_id': self.id, 'text': text, 'parse_mode': 'HTML'}
        try:
            requests.post(url + 'sendMessage', params=params, proxies=proxies)
        except requests.exceptions.ConnectionError as e:
            raise type(e)('Can\'t connect to Telegram servers to send message.')


class Media:
    """
    This is base class for media files, which can be obtained from Telegram API.
    Provides methods for getting file path, downloading file, and
    recognition of media objects. These methods are common for all media objects.
    """

    def __init__(self):
        self.file_path = None
        self.content = None
        self.meta = None

    def get_filepath(self):
        """
        Gets direct link to media file sent by user.
        """
        params = {'file_id': self.file_id}

        try:
            response = requests.get(url + 'getFile', params=params, proxies=proxies)
        except requests.exceptions.ConnectionError as e:
            print('excepted')
            raise type(e)('Can\'t connect to Telegram servers to get file path.')
        else:
            json = response.json()
            print(json)

        try:
            self.file_path = json['result']['file_path']
        except KeyError:
            error = json['error_code']
            description = json['description']
            raise exceptions.tg_errors[error](description)

    def get_file(self):
        """
        Downloads media file sent by user.
        """
        try:
            response = requests.get(url_file + self.file_path, proxies=proxies)
        except requests.exceptions.ConnectionError as e:
            raise type(e)('Can\'t connect to Telegram servers to download file.')
        except TypeError:
            self.get_filepath()
            self.get_file()
        else:
            self.content = response.content

    def recognize(self, offset=0):
        """
        Trying to recognize binary representation of media file
        by querying ACRCloud API.
        :param offset: Skips offset-1 seconds from the start.
        :return: Response as JSON.
        """
        if not self.content:
            self.get_file()

        re = get_recognizer()
        response = re.recognize_by_filebuffer(self.content, offset)
        meta = loads(response)
        return meta

    def get_music_meta(self, meta):
        """
        Extracts music's meta information from API's response JSON object.
        :param meta: Response as JSON.
        """
        status = meta['status']['code']

        if not status:
            self.meta = Meta(meta['metadata']['music'][0])
        else:
            raise exceptions.acr_errors[status](meta['status']['msg'])


class Meta:
    """
    Represents meta information received from ACRCloud API.
    Meta object is a part of Media object.
    Some fields from API response may have been omitted.
    """

    def __init__(self, meta):
        self.isrc = meta.get('external_ids').get('isrc')
        self.upc = meta.get('external_ids').get('upc')
        self.spotify = meta.get('external_metadata', {}).get('spotify')
        self.genres = meta.get('genres')
        self.label = meta.get('label')
        self.release_date = meta.get('release_date')
        self.artists = meta.get('artists')
        self.title = meta.get('title')
        self.album = meta.get('album', {}).get('name')

        self._parse_genres()
        self._parse_artists()
        self._parse_date()

    def _parse_genres(self):
        """
        Flattens genres structure obtained from ACRCloud API's response.
        """
        try:
            self.genres = tuple(genre['name'] for genre in self.genres)
        except TypeError:
            print('No genres were provided.')

    def _parse_artists(self):
        """
        Flattens artists structure obtained from ACRCloud API's response.
        """
        self.artists = tuple(artist['name'] for artist in self.artists)

    def _parse_date(self):
        """
        Converts string representation of a date,
        received from ACRCloud API's response, to 'dddd, MMMM d, yyyy' format.
        """
        d = date.fromisoformat(self.release_date)
        self.release_date = d.strftime('%A, %B %e, %Y')

    def get_info(self):
        """
        Creates formatted output of meta information.
        """
        if self.genres:
            genres = ', '.join(self.genres)
        else:
            genres = None
        artists = ', '.join(self.artists)
        artists = artists.replace(',', ' ft.', 1)

        values = (('', self.title),
                  (' - ', artists),
                  ('Album: ', self.album),
                  ('Release: ', self.release_date),
                  ('Label: ', self.label),
                  ('Genres: ', genres))
        formatted = []
        for prefix, value in values:
            if value:
                formatted_str = Template(prefix + '$val').substitute(val=value)
                formatted.append(formatted_str)
        formatted[0:2] = ['<b>' + formatted[0] + formatted[1] + '</b>']
        output = '\n'.join(formatted)
        return output.strip()

    def __str__(self):
        return self.get_info()


class Audio(Media):
    """
    Represents audio file meta information received from Telegram API update.
    """

    def __init__(self, audio):
        """
        :param audio: Audio object from Telegram API.
        """
        super().__init__()
        self.file_id = audio.get('file_id')
        self.duration = audio.get('duration')
        self.performer = audio.get('performer')
        self.title = audio.get('title')
        self.mime_type = audio.get('mime_type')
        self.file_size = audio.get('file_size')


class Video(Media):
    """
    Represents video file meta information received from Telegram API update.
    """

    def __init__(self, vid):
        """
        :param vid: Video object from Telegram API.
        """
        super().__init__()
        self.file_id = vid.get('file_id')
        self.mime_type = vid.get('mime_type')
        self.file_size = vid.get('file_size')


class Voice(Media):
    """
    Represents voice note meta information received from Telegram API update.
    """

    def __init__(self, voice):
        """
        :param voice: Voice object from Telegram API.
        """
        super().__init__()
        self.file_id = voice.get('file_id')
        self.duration = voice.get('duration')
        self.mime_type = voice.get('mime_type')
        self.file_size = voice.get('file_size')


class VideoNote(Media):
    """
    Represents video note meta information received from Telegram API update.
    """

    def __init__(self, vid_note):
        """
        :param vid_note: Video note object from Telegram API.
        """
        super().__init__()
        self.file_id = vid_note.get('file_id')
        self.duration = vid_note.get('duration')
        self.file_size = vid_note.get('file_size')


# Not implemented yet.
class Entities:
    """
    Represent urls in a message text.
    """

    def __init__(self, entity):
        """
        :param entity: Entity object from Telegram API.
        """
        self.type = entity.get('type')
        self.url = entity.get('url')


if __name__ == '__main__':
    vc_note = Voice({'file_id': 'fe98f8f93j0fqh', 'mime_type': 'audio/mpeg',
                     'duration': 12, 'file_size': 25})
    vc_note.content = 'music/Em_Ri_LWYL.mp3'
    vc_note.recognize()
    print(vc_note.meta)
