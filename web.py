from flask import Flask, session, redirect, url_for, jsonify
import redis
from keys import DISCORD_API_BASE_URL, OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET, REDIS_HOST, REDIS_PORT, WEB_APP_SECRET_KEY
from polycule import Polycule
from authlib.integrations.flask_client import OAuth
from flask_session import Session

AUTHORIZATION_BASE_URL = f'{DISCORD_API_BASE_URL}/oauth2/authorize'
TOKEN_URL = f'{DISCORD_API_BASE_URL}/oauth2/token'

app = Flask(__name__)
app.debug = True
oauth = OAuth(app)
app.secret_key = WEB_APP_SECRET_KEY

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=int(REDIS_PORT),
)

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis_client

server_session = Session(app)

oauth.register(
    name='discord',
    client_id=OAUTH2_CLIENT_ID,
    client_secret=OAUTH2_CLIENT_SECRET,
    access_token_url=TOKEN_URL,
    authorize_url=AUTHORIZATION_BASE_URL,
    api_base_url=DISCORD_API_BASE_URL,
    client_kwargs={'scope': 'identify'}
)

@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.discord.authorize_redirect(redirect_uri)

@app.route('/callback')
def auth():
    oauth.discord.authorize_access_token()
    next_url = session.get('next_url')
    session.pop('next_url', None)

    session['user'] = oauth.discord.get(DISCORD_API_BASE_URL + '/users/@me').json()['id']

    return redirect(next_url)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/me')
def me():
    user = oauth.discord.get(DISCORD_API_BASE_URL + '/users/@me').json()
    return jsonify(user=user)

@app.route("/polycule/<guid>")
def polycule(guid):
    user = session.get('user')
    if user:
        user = int(user)
        cule = Polycule(guid)
        if cule.is_user_registered(user):
            return Polycule(guid).render_graph_to_html()
        else:
            return "Unauthorized access", 401
    else:
        session['next_url'] = url_for('.polycule', guid=guid)
        return redirect(url_for('.login'))

def migrate():
    pass


if __name__ == '__main__':
    app.run()