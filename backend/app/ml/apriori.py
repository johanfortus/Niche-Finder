from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

def perform_apriori(start_date, end_date, country, engagement, tags):
    print('PERFORMING APRIORI')
    print('------------------')