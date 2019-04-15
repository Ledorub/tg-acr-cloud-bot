# Telegram API
token = ''

# Webhook URL.
url = f'https://example.com/bot/{token}/'

# Bot files URL.
url_file = f'https://api.telegram.org/file/bot{token}/'

# Tor proxy. If Telegram servers are blocked.
https_proxy = 'socks5://127.0.0.1:9050'
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
