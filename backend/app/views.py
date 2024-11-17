from flask import render_template, redirect, request, Blueprint, jsonify
from .ml import kmeans, apriori

views = Blueprint('views', __name__)

@views.route('/')
def home_page():
    return render_template('home.html')


@views.route('/result', methods = ['POST'])
def result_page():

    data = request.get_json()
    print(f'{data} \n')

    search_type:str = data['searchType']

    start_date: str = data['dateRange']['start']
    end_date: str = data['dateRange']['end']
    country: str = data['country']
    engagement: str = data['engagement']
    tags: list = data['tags']

    if search_type == 'k-means':
        kmeans.perform_kmeans(data)
    elif search_type == 'apriori':
        apriori.perform_apriori(data)

    return jsonify(data)