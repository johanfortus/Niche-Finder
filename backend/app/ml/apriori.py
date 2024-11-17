def perform_apriori(data):
    print('PERFORMING APRIORI')
    print('------------------')

    
    start_date = data['dateRange']['start']
    end_date = data['dateRange']['end']
    country = data['country']
    engagement = data['engagement']
    tags = data['tags']

    print(f'Date Range: {start_date} - {end_date}')
    print(f'Country: {country}')
    print(f'Engagement: {engagement}')
    print(f'Tags: {tags}')
    print()
    print("search_type type: ", type(data['searchType']))
    print("start_date type: ", type(start_date))
    print("end_date type: ",type(end_date))
    print("country type: ",type(country))
    print("engagement type: ",type(engagement))
    print("tags type: ",type(tags))