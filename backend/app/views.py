from flask import render_template, redirect, request, Blueprint

views = Blueprint('views', __name__)

@views.route('/')
def home_page():
    return render_template('home.html')

# @views.route('/result', methods = ['POST'])
# def result_page():
#     start_date = request.form['startDate']
#     end_date = request.form['endDate']
#     country = request.form['country']
#     engagement = request.form['engagementRange']

#     return render_template('result.html' , start_date=start_date, end_date=end_date, country=country, engagement=engagement)

@views.route('/result', methods = ['POST'])
def result_page():
    data = request.get_json()
    start_date = data['dateRange']['start']
    end_date = data['dateRange']['end']
    country = data['country']
    engagement = data['engagement']

    return render_template('result.html' , start_date=start_date, end_date=end_date, country=country, engagement=engagement)

