from flask import Flask
from google_cloud_ndbm.flask import bind

app = Flask(__name__)
bind(app, "wot-online-hours")


@app.route('/')
def main():
    return 'Backend OK'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
