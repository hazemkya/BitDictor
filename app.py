from flask import Flask, template_rendered, url_for, flash, redirect
from flask.templating import render_template
from forms import prediction

app = Flask(__name__)

app.config['SECRET_KEY'] = '78db24c57'
@app.route("/")
@app.route('/home')
def home():

    return render_template('home.html', title= 'Home')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    form = prediction()
    if form.validate_on_submit():
        if form.days_to_predict.data == 1:
            flash(f'Predicting for {form.days_to_predict.data} day..', 'success')
        else:
            flash(f'Predicting for {form.days_to_predict.data} days..', 'success')
        return redirect(url_for('home'))
    return render_template('prediction.html', title= 'Home', form = form)


@app.route("/documentation")
def documentation():
    return render_template('documentation.html', title='Documentation')


if __name__ == '__main__':
    app.run(debug=True)