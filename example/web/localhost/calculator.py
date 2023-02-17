from flask import Flask, render_template, request, url_for, redirect, g
from pipeline_integrity.material import Material
from pipeline_integrity.pipe import Pipe
from pipeline_integrity.method.asme_b31g import Context, State
from pipeline_integrity.i18n import Lang
from i18n import activate

model = Context(Pipe(11200, 1420, 16, Material("Steel", 295), 7
).add_metal_loss(1000, 100, 10, 20, 1))

app = Flask(__name__)

lang_code = Lang.Ru
activate(lang_code)


@app.route('/')
def main():
    g.asme_url = url_for('asme')
    return render_template('main.html', g=g)


@app.route('/asme/', methods=['GET', 'POST'])
def asme():
    g.asme_url = url_for('asme')
    if request.method == 'POST':
        model.anomaly.pipe.diameter = float(request.form['diameter'])
        model.anomaly.pipe.wallthickness = float(request.form['wall'])
        model.anomaly.pipe.material.yield_strength = float(request.form['smys'])
        model.anomaly.pipe.maop = float(request.form['pressure'])
        model.anomaly.length = float(request.form['length'])
        model.anomaly.depth = float(request.form['depth'])
        return redirect(g.asme_url)

    state = model.pipe_state(is_explain=model.lang(lang_code))

    g.result = _("No danger.")
    if state == State.Replace:
        g.result = _("Replacement of the pipe is necessary.")
    elif state == State.Repair:
        g.result = _("Repair or pressure reduction to {} required.").format(round(model.safe_pressure, 2))

    g.explain = model.explain().replace('\n', '<br>')
    g.asme = model

    return render_template('asme.html', g=g)
