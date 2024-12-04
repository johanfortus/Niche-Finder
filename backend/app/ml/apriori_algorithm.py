import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import kagglehub
import os

def perform_apriori(start_date, end_date, country, engagement, tags, min_support=0.1):
    print('PERFORMING APRIORI')
    print('------------------')
    print('User Input:')
    print(f'Start Date: {start_date}')
    print(f'End Date: {end_date}')
    print(f'Country: {country}')
    print(f'Engagement: {engagement}')
    print(f'Tags: {tags}')
    print()

    path = kagglehub.dataset_download("asaniczka/trending-youtube-videos-113-countries")
    csv_file_path = os.path.join(path, 'trending_yt_videos_113_countries.csv')

    df = pd.read_csv(csv_file_path)


    # Filter out data based on user's search attribute input
    df_filtered = df[(df['publish_date'] >= start_date) & (df['publish_date'] <= end_date) & (df['country'] == country)]
    df_filtered = df_filtered.copy()
    df_filtered['engagement_rate'] = ((df_filtered['like_count'] + df_filtered['comment_count']) / df_filtered['view_count']) * 100
    df_filtered['video_tags'].fillna('', inplace=True)

    engagement = calc_engagement_rate(engagement)
    print(f'Engagement: {engagement}')

    if engagement == 'High':
        df_filtered = df_filtered[df_filtered['engagement_rate'] >= 7]
    elif engagement == 'Moderate':
        df_filtered = df_filtered[(df_filtered['engagement_rate'] >= 3) & (df_filtered['engagement_rate'] < 7)]
    elif engagement == 'Low':
        df_filtered = df_filtered[df_filtered['engagement_rate'] < 3]

    # Clean up dataframe
    df_filtered = df_filtered.copy()
    df_filtered.dropna(subset=['view_count', 'like_count', 'comment_count'], inplace=True)
    df_filtered.drop_duplicates(subset="title", keep="first", inplace=True)
    print(df_filtered)

    # tag prep for apriori
    df_filtered['tag_list'] = df_filtered['video_tags'].apply(
        lambda x: x.replace('"', '').split('|') if isinstance(x, str) else []
    )

    # Filter videos based on user's tags
    if tags:
        df_filtered = df_filtered[
            df_filtered['tag_list'].apply(lambda video_tags: any(user_tag.lower() in [tag.lower() for tag in video_tags] for user_tag in tags))
        ]
        print(f'number of videos after tag filter: {len(df_filtered)}')
        if df_filtered.empty:
            print("No videos with specified tags")
            return None

    # list of *unique* tags
    all_tags = set()
    for tags in df_filtered['tag_list']:
        all_tags.update([tag.strip().lower() for tag in tags])

    # one-hot encoding
    for tag in all_tags:
        df_filtered[tag] = df_filtered['tag_list'].apply(
            lambda x: 1 if tag in [t.strip().lower() for t in x] else 0
        )

    # dataframe prep
    tag_columns = list(all_tags)
    df_tags = df_filtered[tag_columns]

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

    return rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].to_dict(orient='records')

def calc_engagement_rate(engagement):
    # High Engagement(above 7 %): 67 - 100
    # Medium Engagement(between 3 % and 6 %): 33 - 66
    # Low Engagement(between 0 % and 3 %): 0 - 32
    engagement = int(engagement)
    if engagement >= 67:
        return 'High'
    elif engagement <= 66 and engagement >= 33:
        return 'Moderate'
    elif engagement <= 32:
        return 'Low'

# csv path
# csv_file_path = '/Users/vincentmilland/PycharmProjects/PythonProject6/filtered_trending_yt_videos.csv'  # Replace with your actual CSV file path

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
# rules = perform_apriori(csv_file_path, sim_start_date, sim_end_date, sim_country, sim_min_support)
