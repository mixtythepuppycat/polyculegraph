from os import getenv
import os

# Discord API bot token
BOT_TOKEN: str = getenv('BOT_TOKEN')

# Root URL for where the web app is being served from
URL_HOST: str = getenv('URL_HOST', "http://localhost:5000")

# Discord API OAuth2 client ID
OAUTH2_CLIENT_ID: str = getenv('OAUTH2_CLIENT_ID')

# Discord API OAuth2 client secret
OAUTH2_CLIENT_SECRET: str = getenv('OAUTH2_CLIENT_SECRET')

# Discord API OAuth2 client redirect
OAUTH2_REDIRECT_URI: str = getenv('OAUTH2_REDIRECT_URI', f"{URL_HOST}/callback")

# Discord API base URL
DISCORD_API_BASE_URL = getenv('API_BASE_URL', 'https://discordapp.com/api')

# A generated unique secret token for web app security
# See https://docs.python.org/3/library/secrets.html#secrets.token_hex
WEB_APP_SECRET_KEY = getenv('WEB_APP_SECRET_KEY')

# Folder to store graph data
DATA_FOLDER = getenv('DATA_FOLDER', "graph_data")

# Redis host name
REDIS_HOST = getenv('REDIS_HOST', "127.0.0.1")

# Redis port
REDIS_PORT = getenv('REDIS_PORT', "6379")

# Version for displaying in the web app, gets set as part of the docker build
APP_VERSION = getenv('APP_VERSION', "LATEST")