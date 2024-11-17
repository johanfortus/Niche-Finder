from sklearn.cluster import KMeans
import pandas as pd

simulated_data = {
    'searchType': 'k-means',
    'dateRange': {'start': '2024-11-01', 'end': '2024-11-17'},
    'country': 'Spain',
    'engagement': '72',
    'tags': ['sports', 'soccer']
}

sim_start_date = simulated_data['dateRange']['start']
sim_end_date = simulated_data['dateRange']['end']
sim_country = simulated_data['country']
sim_engagement = simulated_data['engagement']

print(f'Start Date: {sim_start_date}')
print(f'End Date: {sim_end_date}')
print(f'Country: {sim_country}')
print(f'Engagement: {sim_engagement}')

def perform_kmeans(start_date, end_date, country, engagement):
    print('PERFORMING K-MEANS')
    print('------------------')



# print(perform_kmeans(sim_start_date, sim_end_date, sim_country, sim_engagement))