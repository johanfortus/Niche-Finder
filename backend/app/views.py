from flask import render_template, redirect, request, Blueprint, jsonify
from .ml import kmeans, apriori

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
    print(f'{data} \n')

    search_type = data['searchType']

    if search_type == 'k-means':
        kmeans.perform_kmeans(data)
    elif search_type == 'apriori':
        apriori.perform_apriori(data)



    # print("search_type type: ", type(search_type))
    # print("start_date type: ", type(start_date))
    # print("end_date type: ",type(end_date))
    # print("country type: ",type(country))
    # print("engagement type: ",type(engagement))
    # print("tags type: ",type(tags))

    return jsonify(data)