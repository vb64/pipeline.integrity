from flask import Flask, render_template, request, url_for, g

from pipeline_integrity.material import Material
from pipeline_integrity.pipe import Pipe
from pipeline_integrity.method.asme_b31g import Context, State

model = Context(Pipe(
  11200,
  1420,
  16,
  Material("Steel", 295),
  7
).add_metal_loss(
  1000,
  100,
  10,
  20,
  1
))

app = Flask(__name__)


@app.route('/')
def main():
    g.asme_url = url_for('asme')
    return render_template('main.html', g=g)


@app.route('/asme/', methods=['GET', 'POST'])
def asme():
    g.asme = model
    if request.method == 'POST':
        return calc_asme()

    return render_template('asme_input.html', g=g)


def calc_asme():
    g.asme_url = url_for('asme')
    return render_template('asme_output.html', g=g)
