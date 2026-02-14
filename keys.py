from os import getenv

BOT_TOKEN: str = getenv('BOT_TOKEN')
URL_HOST: str = getenv('URL_HOST', "http://localhost:5000")
OAUTH2_CLIENT_ID: str = getenv('OAUTH2_CLIENT_ID')
OAUTH2_CLIENT_SECRET: str = getenv('OAUTH2_CLIENT_SECRET')
OAUTH2_REDIRECT_URI: str = getenv('OAUTH2_REDIRECT_URI', f"{URL_HOST}/callback")

DISCORD_API_BASE_URL = getenv('API_BASE_URL', 'https://discordapp.com/api')