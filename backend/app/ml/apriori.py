from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

def perform_apriori(start_date, end_date, country, engagement, tags):
    print('PERFORMING APRIORI')
    print('------------------')


# SIMULATED DATA
'''
simulated_data = {
    'searchType': 'apriori',
    'dateRange': {'start': '2024-11-01', 'end': '2024-11-17'},
    'country': 'Spain',
    'engagement': '72',
    'tags': ['sports', 'soccer']
}

sim_start_date = simulated_data['dateRange']['start']
sim_end_date = simulated_data['dateRange']['end']
sim_country = simulated_data['country']
sim_engagement = simulated_data['engagement']
sim_tags = simulated_data['tags']

print(f'Start Date: {sim_start_date}')
print(f'End Date: {sim_end_date}')
print(f'Country: {sim_country}')
print(f'Engagement: {sim_engagement}')
print(f'Tags: {sim_tags}')

print(perform_apriori(sim_start_date, sim_end_date, sim_country, sim_engagement, sim_tags)) 
'''