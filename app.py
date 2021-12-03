from flask import Flask, sessions, template_rendered, url_for, flash, redirect, session
from flask.templating import render_template
from wtforms.fields.core import Label
from forms import prediction_Input
import model_selection
from rq import Queue
from worker import conn
import time

app = Flask(__name__)
q = Queue('high', connection=conn)
app.config['SECRET_KEY'] = 'BitDictor'


@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    form = prediction_Input()
    days = form.days_to_predict.data
    if form.validate_on_submit():
        if form.days_to_predict.data == 1:
            flash(f'Predicting for {days} day..', 'success')
        else:
            flash(f'Predicting for {days} days..', 'success')
        session['days'] = days
        return redirect(url_for('BitDict'))
    return render_template('prediction.html', title='home', form=form)


@app.route('/BitDict', methods=['GET', 'POST'])
def BitDict():
    form = prediction_Input()
    days = form.days_to_predict.data
    if form.validate_on_submit():
        if form.days_to_predict.data == 1:
            flash(f'Predicting for {days} day..', 'success')
        else:
            flash(f'Predicting for {days} days..', 'success')
        session['days'] = days
        return redirect(url_for('BitDict'))
    if 'days' in session:
        days = session['days']
    else:
        redirect(url_for('home'))
    results = q.enqueue(
        model_selection.get_prediction, days)
    time.sleep(2)
    while results.result == None:
        time.sleep(1)

    print(results)
    print(results.result)
    Labels, values, predicted = results.result
    return render_template('BitDict.html', title='BitDict',
                           form=form, Labels=Labels, values=list(values),
                           table_data=predicted)


if __name__ == '__main__':
    app.run(debug=True)
