# YouTube Niche Finder
Identifying high-performing niches and trends on YouTube to assist aspiring content creators in selecting topics with high engagement potential.

## Summary

Starting a YouTube channel can be challenging for new creators due to the overwhelming competition. Niche Finder simplifies this process by using data-driven techniques to identify high-performing niches, trends, and tags.

This project utilizes Python, Flask, Pandas, and NumPy to process data from the [Top Trending YouTube Videos Dataset](https://www.kaggle.com/datasets/asaniczka/trending-youtube-videos-113-countries/code). K-Means clustering and the FP-Growth algorithm are applied to analyze video groupings and discover frequent tag associations. Dynamic visualizations are created using D3.js to present trends interactively.

Niche Finder helps creators to make informed content decisions with an intuitive, data-focused approach.

## Setup
Obtain a Kaggle API key at https://www.kaggle.com/docs/api to access Kaggle datasets

Next, clone the repository to your local machine
```
$ git clone https://github.com/johanfortus/Niche-Finder/
$ cd Niche-Finder
```
Create and activate a Python virtual environment
```
$ python -m venv venv
$ source venv/bin/activate
```
Install dependencies
```
(venv) $ pip install -r requirements.txt
```
Start server
```
(venv) $ flask run
```
Open http://127.0.0.1:5000/ to view project in the browser.

## Built With
- [<img src="https://img.shields.io/badge/-Python-blue?style=for-the-badge&logo=python&logoColor=FFFF2E" />](https://www.python.org)
- [<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />](https://flask.palletsprojects.com/en/2.2.x/)
- [<img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />](https://scikit-learn.org/)
- [<img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white" />](https://pandas.pydata.org/)
- [<img src="https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white" />](https://numpy.org/)
- [<img src="https://img.shields.io/badge/javascript-%23F7DF1E.svg?&style=for-the-badge&logo=javascript&logoColor=black" />](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [<img src="https://img.shields.io/badge/d3%20js-F9A03C?style=for-the-badge&logo=d3.js&logoColor=white" />](https://d3js.org/)

## Demonstration

<img src="https://github.com/johanfortus/Niche-Finder/blob/main/Demonstration.gif" /> 
