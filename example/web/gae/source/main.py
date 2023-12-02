from flask import Flask, render_template, url_for, g
from google_cloud_ndbm.flask import bind
from i18n import activate, LANG_CODE
from asme import asme_page

app = Flask(__name__)
bind(app, "wot-online-hours")
app.secret_key = b'YourSecretKeyHere'
app.register_blueprint(asme_page)
activate(app, LANG_CODE)


@app.route('/')
def main():
    g.asme_url = url_for('asme_page.show')
    return render_template('main.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
