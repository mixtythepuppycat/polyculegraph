from flask import Flask, render_template, session, redirect, url_for
import redis
from keys import DISCORD_API_BASE_URL, OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET, REDIS_HOST, REDIS_PORT, WEB_APP_SECRET_KEY
from polycule import Polycule, Polycules
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
    
    guilds = oauth.discord.get(DISCORD_API_BASE_URL + '/users/@me/guilds').json()

    # cache their registered polycules in the session
    if not session.get("userPolycules"):
        user = int(session.get('user'))
        session['userPolycules'] = Polycules().is_user_in_polycules(user, [guild["id"] for guild in guilds])

    user_polycules = session['userPolycules']
    found_guilds = [guild for guild in guilds if guild['id'] in user_polycules]

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
    session.pop('userPolycules', None)
    return redirect('/')
    
@app.route("/graph/<guid>")
def graph(guid):
    if not_logged_in(url_for('.graph', guid=guid)):
        return redirect(url_for('.login'))

    user = int(session.get('user'))
    cule = Polycule(guid)
    if cule.is_user_registered(user):
        return Polycule(guid).render_graph_to_html()
    else:
        return "Unauthorized access", 401
    
@app.route("/getting-started")
def getting_started():
    return render_template("getting-started.html")

if __name__ == '__main__':
    app.run()
