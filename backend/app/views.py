from flask import render_template, redirect, request, Blueprint

views = Blueprint('views', __name__)

@views.route('/')
def home_page():
    return render_template('home.html')

@views.route('/result', methods = ['POST'])
def result_page():
    start_date = request.form['start-date']
    end_date = request.form['end-date']
    country = request.form['country']
    engagement = request.form['engagement']

    return render_template('result.html' , start_date=start_date, end_date=end_date, country=country, engagement=engagement)