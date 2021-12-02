from flask import Flask, sessions, template_rendered, url_for, flash, redirect, session
from flask.templating import render_template
from wtforms.fields.core import Label
from forms import prediction_Input
import model_selection

app = Flask(__name__)

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
        redirect(url_for('predict'))
    Labels, values, predicted = model_selection.get_prediction(days)
    return render_template('BitDict.html', title='BitDict',
                           form=form, Labels=Labels, values=list(values),
                           table_data=predicted)


@app.route("/documentation")
def documentation():
    return render_template('documentation.html', title='Documentation')


if __name__ == '__main__':
    app.run(debug=True)
