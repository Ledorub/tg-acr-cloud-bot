# Telegram API
token = ''

# Bot URL.
url = f'https://api.telegram.org/bot{token}/'

# Bot files URL.
url_file = f'https://api.telegram.org/file/bot{token}/'

# If Telegram servers are blocked.
https_proxy = ''
proxies = {
    'http': https_proxy,
    'https': https_proxy
}

# ACRCloud API
acr_config = {
    'host': '',
    'access_key': '',
    'access_secret': '',
    'timeout': 5
}

# Webhook URL.
url_wh = f'example.com/bot/{token}'
