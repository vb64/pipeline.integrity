# https://flask.palletsprojects.com/en/2.2.x/blueprints/
from flask import Blueprint, render_template, request, url_for, redirect, session, g
from google.cloud import ndb
from google.protobuf.message import DecodeError
from pipeline_integrity.material import Material
from pipeline_integrity.pipe import Pipe
from pipeline_integrity.method.asme_b31g import Context, State
from i18n import LANG_CODE

asme_page = Blueprint('asme_page', __name__)


class AsmeB31G(ndb.Model):
    last_used = ndb.DateTimeProperty(indexed=True, auto_now=True)
    diameter = ndb.FloatProperty(indexed=False, default=1420.0)
    wallthickness = ndb.FloatProperty(indexed=False, default=16.0)
    smys = ndb.FloatProperty(indexed=False, default=295.0)
    maop = ndb.FloatProperty(indexed=False, default=7.0)
    length = ndb.FloatProperty(indexed=False, default=100.0)
    depth = ndb.FloatProperty(indexed=False, default=1.0)


@asme_page.route('/asme/', methods=['GET', 'POST'])
def show():
    if 'session_id' in session:
        try:
            asme = ndb.Key(urlsafe=session['session_id']).get()
        except DecodeError:
            asme = None
        if not asme:
            asme = AsmeB31G()
            session['session_id'] = asme.put().urlsafe()
    else:
        asme = AsmeB31G()
        session['session_id'] = asme.put().urlsafe()

    g.asme_url = url_for('asme_page.show')
    if request.method == 'POST':
        save_form(asme, request.form)
        return redirect(g.asme_url)

    model = get_model(asme)
    state = model.pipe_state(is_explain=model.lang(LANG_CODE))
    g.result = _("No danger.")

    if state == State.Replace:
        g.result = _("Replacement of the pipe is necessary.")
    elif state == State.Repair:
        g.result = _("Repair or pressure reduction to {} required.").format(round(model.safe_pressure, 2))

    g.explain = model.explain().replace('\n', '<br>')
    g.asme = model

    return render_template('asme.html', g=g)


def get_model(asme):
    model = Context(
      Pipe(11200, 1420, 16, Material("Steel", 295), 7
    ).add_metal_loss(1000, 100, 10, 20, 1))

    pipe = model.anomaly.pipe

    pipe.diameter = asme.diameter
    pipe.wallthickness = asme.wallthickness
    pipe.material.yield_strength = asme.smys
    pipe.maop = asme.maop

    model.anomaly.length = asme.length
    model.anomaly.depth = asme.depth

    return model


def save_form(asme, form):
    asme.diameter = float(form['diameter'])
    asme.wallthickness = float(form['wall'])
    asme.smys = float(form['smys'])
    asme.maop = float(form['pressure'])
    asme.length = float(form['length'])
    asme.depth = float(form['depth'])
    return asme.put()
