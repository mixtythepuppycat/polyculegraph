from functools import wraps
import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import redis
from keys import DISCORD_API_BASE_URL, DATA_FOLDER, OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET, REDIS_HOST, REDIS_PORT, WEB_APP_SECRET_KEY
from polycule import Polycule
from authlib.integrations.flask_client import OAuth
from flask_session import Session

AUTHORIZATION_BASE_URL = f'{DISCORD_API_BASE_URL}/oauth2/authorize'
TOKEN_URL = f'{DISCORD_API_BASE_URL}/oauth2/token'

app = Flask(__name__)
app.debug = True
oauth = OAuth(app)
app.secret_key = WEB_APP_SECRET_KEY

if __name__ != '__main__':
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=int(REDIS_PORT),
    )

    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = redis_client

    server_session = Session(app)


def set_token(token):
    session['token_type'] = token.get('token_type')
    session['access_token'] = token.get('access_token')
    session['refresh_token'] = token.get('refresh_token')
    session['expires_at'] = token.get('expires_at')

def fetch_token():
    return dict(
        access_token=session.get('access_token'),
        token_type=session.get('token_type'),
        refresh_token=session.get('refresh_token'),
        expires_at=session.get('expires_at')
    )

def update_token(name, token, refresh_token=None, access_token=None):
    session['access_token'] = token.get('access_token')
    session['refresh_token'] = token.get('refresh_token')
    session['expires_at'] = token.get('expires_at')


oauth.register(
    name='discord',
    client_id=OAUTH2_CLIENT_ID,
    client_secret=OAUTH2_CLIENT_SECRET,
    access_token_url=TOKEN_URL,
    authorize_url=AUTHORIZATION_BASE_URL,
    api_base_url=DISCORD_API_BASE_URL,
    fetch_token=fetch_token,
    update_token=update_token,
    client_kwargs={'scope': 'identify guilds'}
)

def not_logged_in(current_url):
    if not session.get('user'):
        session['next_url'] = current_url
        return True
    else:
        return False

@app.route('/')
def root():
    if not_logged_in('/'):
        return redirect(url_for('.login'))
    
    found_guilds = []
    guilds = oauth.discord.get(DISCORD_API_BASE_URL + '/users/@me/guilds').json()
    for guild in guilds:
        id = guild["id"]
        if(os.path.exists(f"{DATA_FOLDER}/{id}.gml")):
            found_guilds.append(guild)

    return render_template("root.html", 
                           title="Polycule Graph",
                           guilds=found_guilds)

@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.discord.authorize_redirect(redirect_uri)

@app.route('/callback')
def auth():
    set_token(oauth.discord.authorize_access_token())
    next_url = session.get('next_url')
    session.pop('next_url', None)

    session['user'] = oauth.discord.get(DISCORD_API_BASE_URL + '/users/@me').json()['id']

    return redirect(next_url)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/guild')
def guild():
    if not_logged_in(url_for('.guild')):
        return redirect(url_for('.login'))

    guilds = oauth.discord.get(DISCORD_API_BASE_URL + '/users/@me/guilds').json()
    guild_id = "1409568706740224143"
    result = [x for x in guilds if x["id"] == guild_id]
    hash = result[0].get("icon")
    guild_name = result[0].get("name")
    icon_url = f"https://cdn.discordapp.com/icons/{guild_id}/{hash}.png"
    
    return jsonify(icon_url=icon_url, guild_name=guild_name, guilds=guilds)

@app.route('/me')
def me():
    if not_logged_in(url_for('.me')):
        return redirect(url_for('.login'))

    user = oauth.discord.get(DISCORD_API_BASE_URL + '/users/@me').json()
    return jsonify(user=user)

@app.route("/polycule/<guid>")
def polycule(guid):
    if not_logged_in(url_for('.polycule', guid=guid)):
        return redirect(url_for('.login'))

    guilds = oauth.discord.get(DISCORD_API_BASE_URL + '/users/@me/guilds').json()
    result = [x for x in guilds if x["id"] == guid]
    hash = result[0].get("icon")
    guild_name = result[0].get("name")
    icon_url = f"https://cdn.discordapp.com/icons/{guid}/{hash}.png"

    user = int(session.get('user'))
    cule = Polycule(guid)
    if cule.is_user_registered(user):
        return render_template("polycule.html", 
                               graph=Polycule(guid).render_graph_to_html(),
                               icon=icon_url,
                               name=guild_name)
    else:
        return "Unauthorized access", 401
    
@app.route("/getting-started")
def getting_started():
    return render_template("getting-started.html")

if __name__ == '__main__':
    app.run()
