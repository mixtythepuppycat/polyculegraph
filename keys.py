from os import getenv

BOT_TOKEN: str = getenv('BOT_TOKEN')
URL_HOST: str = getenv('URL_HOST', "http://localhost:5000")