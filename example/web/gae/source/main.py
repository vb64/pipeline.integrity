import os
from flask import Flask, render_template, url_for, g
from google.cloud import ndb
from i18n import activate
from asme import asme_page

# https://stackoverflow.com/questions/43628002/google-vision-api-project-not-passed
os.environ["GCLOUD_PROJECT"] = "wot-online-hours"
client = ndb.Client()

def ndb_wsgi_middleware(wsgi_app):
    def middleware(environ, start_response):
        with client.context():
            return wsgi_app(environ, start_response)

    return middleware


app = Flask(__name__)
app.wsgi_app = ndb_wsgi_middleware(app.wsgi_app)  # Wrap the app in middleware.
app.secret_key = b'YourSecretKeyHere'
app.register_blueprint(asme_page)
activate(app, 'ru')


@app.route('/')
def main():
    g.asme_url = url_for('asme_page.show')
    return render_template('main.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
