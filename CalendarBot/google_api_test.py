import os
import flask
import google_auth_oauthlib.flow
from CalendarBot.web_site_create_api import blueprint

app = flask.Flask(__name__)

app.secret_key = 'us!m.Mi4qkbLJovhap_82-TXc3'


@app.route('/')
def main():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/calendar'])
    flow.redirect_uri = flask.url_for('authorization', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    flask.session['state'] = state
    return flask.redirect(authorization_url)


@app.route('/authorization')
def authorization():
    state = flask.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json', scopes=['https://www.googleapis.com/auth/calendar'], state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)
    return 'Вы успешно авторизировались!'


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.register_blueprint(blueprint)
    app.run()
