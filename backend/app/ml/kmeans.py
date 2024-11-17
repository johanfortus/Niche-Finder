from sklearn.cluster import KMeans
import pandas as pd



def perform_kmeans(data):
    print('PERFORMING K-MEANS')
    print('------------------')
    start_date = data['dateRange']['start']
    end_date = data['dateRange']['end']
    country = data['country']
    engagement = data['engagement']
