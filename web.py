import os
from flask import Flask, g, make_response, session, redirect, request, url_for, jsonify
from requests_oauthlib import OAuth2Session
from keys import DISCORD_API_BASE_URL, OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET, OAUTH2_REDIRECT_URI
from polycule import Polycule
from authlib.integrations.flask_client import OAuth

AUTHORIZATION_BASE_URL = f'{DISCORD_API_BASE_URL}/oauth2/authorize'
TOKEN_URL = f'{DISCORD_API_BASE_URL}/oauth2/token'

app = Flask(__name__)
app.debug = True
oauth = OAuth(app)
app.secret_key = OAUTH2_CLIENT_SECRET

oauth.register(
    name='discord',
    client_id=OAUTH2_CLIENT_ID,
    client_secret=OAUTH2_CLIENT_SECRET,
    access_token_url=TOKEN_URL,
    access_token_params=None,
    authorize_url=AUTHORIZATION_BASE_URL,
    authorize_params=None,
    api_base_url=DISCORD_API_BASE_URL,
    fetch_token=lambda: session.get('token'),  # DON'T DO IT IN PRODUCTION
    client_kwargs={'scope': 'identify'}
)

#if 'http://' in OAUTH2_REDIRECT_URI:
#    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

#@app.route('/')
#def homepage():
#    user = session.get('user')
#    return render_template('home.html', user=user)


@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    session['next_url'] = request.args.get('next_url')

    return oauth.discord.authorize_redirect(redirect_uri, next_url=request.args.get('next_url'))


@app.route('/callback')
def auth():
    token = oauth.discord.authorize_access_token()
    session['token'] = token
    next_url = session.get('next_url')
    session.pop('next_url', None)

    session['user'] = oauth.discord.get(DISCORD_API_BASE_URL + '/users/@me').json()['id']

    #return redirect(url_for(f'.polycule/{session.get('requested_cule')}'))
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
    token = session.get('token')
    if token:
        user = int(session.get('user'))
        cule = Polycule(guid)
        if cule.is_user_registered(user):
            return Polycule(guid).render_graph_to_html()
        else:
            return make_response(jsonify({'error': 'Unauthorized access'}), 401)
    else:
        #session['requested_cule'] = guid
        return redirect(url_for('.login', next_url=url_for('.polycule', guid=guid)))

def migrate():
    pass


if __name__ == '__main__':
    app.run()