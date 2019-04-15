"""
Provides exceptions for both Telegram API and ACRCloud API.
"""

# TELEGRAM

class TelegramApiError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BadRequest(TelegramApiError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Unauthorized(TelegramApiError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Forbidden(TelegramApiError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NotFound(TelegramApiError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Flood(TelegramApiError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Internal(TelegramApiError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


tg_errors = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    420: Flood,
    500: Internal,
}


# ACRCloud

class AcrCloudApiError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ServiceError(AcrCloudApiError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RecognitionError(AcrCloudApiError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class UnknownError(AcrCloudApiError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


acr_errors = {
    1001: RecognitionError,
    2000: ServiceError,
    2001: ServiceError,
    2002: RecognitionError,
    2004: RecognitionError,
    2005: ServiceError,
    2010: UnknownError,
    3000: ServiceError,
}
