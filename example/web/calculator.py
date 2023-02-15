from flask import Flask, render_template, request, url_for, g

app = Flask(__name__)

@app.route('/')
def main():
    g.asme_url = url_for('asme')
    return render_template('main.html', g=g)


@app.route('/asme/', methods=['GET', 'POST'])
def asme():
    if request.method == 'POST':
        return calc_asme()
    return render_template('asme_input.html')


def calc_asme():
    g.asme_url = url_for('asme')
    return render_template('asme_output.html', g=g)
