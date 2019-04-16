from acrcloud.recognizer import ACRCloudRecognizer
from acr_bot.config import acr_config


def get_recognizer():
    """
    Gets recognizer with parameters from config.
    :return: Recognizer.
    """
    return ACRCloudRecognizer(acr_config)


if __name__ == '__main__':
    print(get_recognizer().recognize_by_file('music/audiofile.mp3', 0))
