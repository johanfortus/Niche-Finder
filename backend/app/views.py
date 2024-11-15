from flask import render_template, redirect, request, Blueprint

views = Blueprint('views', __name__)

@views.route('/')
def home_page():
    return

@views.route('/result', methods = ['POST'])
def result_page():
    return