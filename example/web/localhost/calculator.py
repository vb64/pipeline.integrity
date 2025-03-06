import os
from flask import Flask, render_template, request, url_for, redirect, g
from pipeline_material import PipeMaterial as Material
from pipeline_integrity.pipe import Pipe
from pipeline_integrity.method.asme.b31g_1991 import Context, State
from pipeline_integrity.i18n import Lang
from i18n import activate

model = Context(Pipe(11200, 1420, 16, Material("Steel", 295), 7
).add_metal_loss(1000, 100, 10, 20, 1))

app = Flask(__name__)
lang_code = os.getenv('LANG_CODE')
activate(app, lang_code)

lang = True
if lang_code in [Lang.Ru]:
    lang = model.lang(lang_code)


@app.route('/')
def main():
    g.asme_url = url_for('asme')
    return render_template('main.html', g=g)


@app.route('/asme/', methods=['GET', 'POST'])
def asme():
    g.asme_url = url_for('asme')
    if request.method == 'POST':
        save_form(model.anomaly, request.form)
        return redirect(g.asme_url)

    state = model.pipe_state(is_explain=lang)

    g.result = _("No danger.")
    if state == State.Replace:
        g.result = _("Replacement of the pipe is necessary.")
    elif state == State.Repair:
        g.result = _("Repair or pressure reduction to {} required.").format(round(model.safe_pressure, 2))

    g.explain = model.explain().replace('\n', '<br>')
    g.asme = model

    return render_template('asme.html', g=g)

def save_form(defect, form):
    pipe = defect.pipe
    pipe.diameter = float(form['diameter'])
    pipe.wallthickness = float(form['wall'])
    pipe.material.yield_strength = float(form['smys'])
    pipe.maop = float(form['pressure'])

    defect.length = float(form['length'])
    defect.depth = float(form['depth'])
