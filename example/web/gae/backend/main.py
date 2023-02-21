import logging
from datetime import datetime, timedelta
from flask import Flask
from google.cloud import ndb
from google_cloud_ndbm.flask import bind

app = Flask(__name__)
bind(app, "wot-online-hours")


class AsmeB31G(ndb.Model):
    last_used = ndb.DateTimeProperty(indexed=True, auto_now=True)


@app.route('/')
def main():
    border = datetime.utcnow() - timedelta(days=14)
    query = AsmeB31G.query(AsmeB31G.last_used < border)
    keys = query.fetch(100, keys_only=True)
    if keys:
        ndb.model.delete_multi(keys)

    logging.warning("### Purge old AsmeB31G keys: %s", len(keys))

    return 'AsmeB31G keys: {}'.format(len(keys))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
