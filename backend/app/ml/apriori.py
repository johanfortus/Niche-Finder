import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def perform_apriori(csv_file_path, start_date, end_date, country, min_support):
    print('PERFORMING APRIORI')
    print('------------------')

    # load dataset
    try:
        df = pd.read_csv(csv_file_path, encoding='utf-8')
    except FileNotFoundError:
        print(f"Dataset file '{csv_file_path}' not found.")
        return None

    # print the columns to verify
    print("Columns in DataFrame:", df.columns.tolist())

    # country column check
    if 'country' not in df.columns:
        print("The dataset does not contain a 'country' column.")
        return None

    # date and time conversion
    if 'publish_date' in df.columns:
        # Adjust the date format as per your data
        # For example, if 'publish_date' is in 'YYYY-MM-DD' format
        df['publish_date'] = pd.to_datetime(df['publish_date'], format='%Y-%m-%d', errors='coerce')
        date_column = 'publish_date'
    else:
        print("No suitable date column ('publish_date') found in the dataset.")
        return None

    # filters invalid dates
    df = df.dropna(subset=[date_column])

    # filters rest of data
    mask = (df[date_column] >= pd.to_datetime(start_date)) & \
           (df[date_column] <= pd.to_datetime(end_date)) & \
           (df['country'].str.lower() == country.lower())
    df_filtered = df.loc[mask].copy()

    if df_filtered.empty:
        print("No data found for the given date range and country.")
        return None

    # engagement rate calculation
    df_filtered['engagement_rate'] = ((df_filtered['like_count'] + df_filtered['comment_count']) / df_filtered['view_count']) * 100
    df_filtered['engagement_rate'] = df_filtered['engagement_rate'].replace([float('inf'), -float('inf')], 0)
    df_filtered['engagement_rate'] = df_filtered['engagement_rate'].fillna(0)

    # categorizingh basedo on engagement
    def categorize_engagement(rate):
        if rate >= 5:
            return 'High'
        elif 2 <= rate < 5:
            return 'Moderate'
        else:
            return 'Low'

    df_filtered['engagement_level'] = df_filtered['engagement_rate'].apply(categorize_engagement)

    # high engagement only
    df_high_engagement = df_filtered[df_filtered['engagement_level'] == 'High'].copy()

    if df_high_engagement.empty:
        print("No high-engagement videos found.")
        return None

    # tag prep for apriori
    df_high_engagement['tag_list'] = df_high_engagement['video_tags'].apply(
        lambda x: x.replace('"', '').split('|'))

    # list of *unique* tags
    all_tags = set()
    for tags in df_high_engagement['tag_list']:
        all_tags.update([tag.strip().lower() for tag in tags])

    # one-hot encoding
    for tag in all_tags:
        df_high_engagement[tag] = df_high_engagement['tag_list'].apply(
            lambda x: 1 if tag in [t.strip().lower() for t in x] else 0
        )

    # dataframe prep
    tag_columns = list(all_tags)
    df_tags = df_high_engagement[tag_columns]

    # convert to bool
    df_tags = df_tags.astype(bool)

    # apriori
    frequent_itemsets = apriori(df_tags, min_support=min_support, use_colnames=True)

    if frequent_itemsets.empty:
        print("No frequent itemsets found with the given minimum support.")
        return None

    # association rules
    try:
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)
    except TypeError:
        # this was the fix for a version error by mlxtend
        rules = association_rules(frequent_itemsets, frequent_itemsets.shape[0],
                                  metric="confidence", min_threshold=0.5)

    if rules.empty:
        print("No association rules found with the given minimum threshold.")
        return None

    # print rules
    print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

    return rules

# csv path
csv_file_path = '/Users/vincentmilland/PycharmProjects/PythonProject6/filtered_trending_yt_videos.csv'  # Replace with your actual CSV file path

# simulated input data for testing
simulated_data = {
    'searchType': 'apriori',
    'dateRange': {'start': '2024-09-09', 'end': '2024-10-25'},
    'country': 'US', 
    'min_support': 0.01,
}

sim_start_date = simulated_data['dateRange']['start']
sim_end_date = simulated_data['dateRange']['end']
sim_country = simulated_data['country']
sim_min_support = simulated_data['min_support']

# apriori call for testing
rules = perform_apriori(csv_file_path, sim_start_date, sim_end_date, sim_country, sim_min_support)
