from flask import render_template, redirect, request, Blueprint, jsonify
from .ml import kmeans, fpgrowth
from .constants import *

views = Blueprint('views', __name__)

@views.route('/')
def home_page():
    return render_template('home.html', countries=COUNTRIES)

@views.route('/result', methods = ['POST'])
def result_page():

    data = request.get_json()
    print(f'{data} \n')

    search_type:str = data['searchType']

    start_date: str = data['dateRange']['start']
    end_date: str = data['dateRange']['end']
    country: str = COUNTRIES_MAP[data['country']]
    engagement: int = int(data['engagement'])
    tags: list = data['tags']

    result_data = {}
    if search_type == 'k-means':
        result_data = kmeans.perform_kmeans(start_date, end_date, country, engagement)
    elif search_type == 'apriori':
        result_data = fpgrowth.perform_fpgrowth(start_date, end_date, country, engagement, tags)

    return jsonify(result_data)