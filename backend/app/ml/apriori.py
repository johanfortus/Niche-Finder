def perform_apriori(data):
    print('PERFORMING APRIORI')
    print('------------------')
    start_date = data['dateRange']['start']
    end_date = data['dateRange']['end']
    country = data['country']
    engagement = data['engagement']
    tags = data['tags']