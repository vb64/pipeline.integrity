# https://flask.palletsprojects.com/en/2.2.x/blueprints/
from flask import Blueprint, render_template, request, url_for, redirect, session, g
from google.cloud import ndb
from google.protobuf.message import DecodeError
from pipeline_integrity.material import Material
from pipeline_integrity.pipe import Pipe
from pipeline_integrity.method.asme.b31g_2012 import Context
from i18n import LANG_CODE

asme_page = Blueprint('asme_page', __name__)


class AsmeB31G(ndb.Model):
    last_used = ndb.DateTimeProperty(indexed=True, auto_now=True)
    diameter = ndb.FloatProperty(indexed=False, default=1420.0)
    wallthickness = ndb.FloatProperty(indexed=False, default=16.0)
    smys = ndb.FloatProperty(indexed=False, default=295.0)
    smts = ndb.FloatProperty(indexed=False, default=340.0)
    maop = ndb.FloatProperty(indexed=False, default=7.0)
    length = ndb.FloatProperty(indexed=False, default=100.0)
    depth = ndb.FloatProperty(indexed=False, default=1.0)
    is_modified = ndb.BooleanProperty(indexed=False, default=False)
    corrosion_rate = ndb.FloatProperty(indexed=False, default=0.4)


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
    model.is_explain = model.lang(LANG_CODE)
    years = model.years(is_mod=asme.is_modified)

    if years == 0:
        g.result = _("Repair or pressure reduction to {} required.").format(round(model.safe_pressure, 2))
    elif years > 100:
        g.result = _("Repair not required.")
    else:
        g.result = _("Repair required after years: {}.").format(int(round(years)))

    g.explain = model.explain().replace('\n', '<br>')
    g.asme = model
    g.is_modified = asme.is_modified

    return render_template('asme.html', g=g)


def get_model(asme):
    """Return asme Context for calculation."""
    material = Material("Steel", 295)
    material.smts = 340

    model = Context(
      Pipe(11200, 1420, 16, material, 7
    ).add_metal_loss(1000, 100, 10, 20, 1))

    pipe = model.anomaly.pipe

    pipe.material.smys = asme.smys
    pipe.material.smts = asme.smts
    pipe.diameter = asme.diameter
    pipe.wallthickness = asme.wallthickness
    pipe.maop = asme.maop

    model.anomaly.length = asme.length
    model.anomaly.depth = asme.depth
    model.corrosion_rate = asme.corrosion_rate

    return model


def save_form(asme, form):
    asme.diameter = float(form['diameter'])
    asme.wallthickness = float(form['wall'])
    asme.smys = float(form['smys'])
    asme.smts = float(form['smts'])
    asme.maop = float(form['pressure'])
    asme.length = float(form['length'])
    asme.depth = float(form['depth'])
    asme.corrosion_rate = float(form['corate'])
    asme.is_modified = True if 'modified' in form else False
    return asme.put()
