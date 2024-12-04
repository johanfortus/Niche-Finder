import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
from mlxtend.frequent_patterns import fpgrowth, association_rules
import kagglehub
import os

# Kaggle dataset download
asaniczka_trending_youtube_videos_113_countries_path = kagglehub.dataset_download('asaniczka/trending-youtube-videos-113-countries')
print('Data source import complete.')
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

def perform_fpgrowth(start_date, end_date, country, engagement, min_support=0.001):
    print('PERFORMING FP-GROWTH')
    print('-------------------')

    # load dataset from Kaggle
    # csv_dir_path = asaniczka_trending_youtube_videos_113_countries_path
    # csv_file_path = os.path.join(csv_dir_path, 'trending_yt_videos_113_countries.csv')
    path = kagglehub.dataset_download("asaniczka/trending-youtube-videos-113-countries")
    csv_file_path = os.path.join(path, 'trending_yt_videos_113_countries.csv')

    df = pd.read_csv(csv_file_path)
    df_filtered = df[(df['publish_date'] >= start_date) & (df['publish_date'] <= end_date) & (df['country'] == country)]
    df_filtered = df_filtered.copy()
    df_filtered['engagement_rate'] = ((df_filtered['like_count'] + df_filtered['comment_count']) / df_filtered['view_count']) * 100

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

    df_filtered['tag_list'] = df_filtered['video_tags'].apply(
        lambda x: x.replace('"', '').split('|') if pd.notna(x) else [] )

    # list of *unique* tags
    all_tags = set()
    for tags in df_filtered['tag_list']:
        all_tags.update([tag.strip().lower() for tag in tags])

    if not all_tags:
        print("No tags found in the filtered dataset.")
        return None

    # Remove highly frequent tags
    tag_counts = df_filtered['tag_list'].explode().value_counts()
    threshold = len(df_filtered) * 0.5  # Set threshold at 50% of records
    frequent_tags = tag_counts[tag_counts > threshold].index.tolist()
    df_filtered['tag_list'] = df_filtered['tag_list'].apply(lambda tags: [tag for tag in tags if tag not in frequent_tags])

    # Update list of *unique* tags after removing highly frequent tags
    all_tags = set()
    for tags in df_filtered['tag_list']:
        all_tags.update([tag.strip().lower() for tag in tags])

    if not all_tags:
        print("No tags found in the filtered dataset after removing frequent tags.")
        return None

    # one-hot encoding using numpy for better performance
    tag_dummies = pd.DataFrame(np.zeros((len(df_filtered), len(all_tags)), dtype=int), columns=list(all_tags))
    for i, tags in enumerate(df_filtered['tag_list']):
        for tag in tags:
            tag_dummies.at[i, tag.strip().lower()] = 1

    # combine original DataFrame with tag dummies
    df_tags = pd.concat([df_filtered.reset_index(drop=True), tag_dummies], axis=1)

    # dataframe prep for FP-Growth
    tag_columns = list(all_tags)
    df_tags = df_tags[tag_columns]

    # convert to bool
    df_tags = df_tags.astype(bool)

    # FP-Growth with max_len to limit the size of itemsets
    frequent_itemsets = fpgrowth(df_tags, min_support=0.001, use_colnames=True, max_len=3)

    if frequent_itemsets.empty:
        print("No frequent itemsets found with the given minimum support. Consider lowering the min_support value.")
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

    # filter rules based on lift value to remove redundant ones
    rules = rules[rules['lift'] > 1.5]

    if rules.empty:
        print("No association rules found with the given lift threshold.")
        return None

    # print rules
    print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

    # find the tags with the best engagement
    best_tags = set()
    for antecedents in rules['antecedents']:
        best_tags.update(antecedents)

    print("Tags that produce the best results for engagement:")
    print(best_tags)

    # return best_tags
    return {
        'status': 'success',
        'best_tags': list(best_tags)
    }

# simulated input data for testing
simulated_data = {
    'searchType': 'fpgrowth',
    'dateRange': {'start': '2024-09-09', 'end': '2024-10-25'},
    'country': 'US',
    'engagement': 35,
    'min_support': 0.001,
}

sim_start_date = simulated_data['dateRange']['start']
sim_end_date = simulated_data['dateRange']['end']
sim_country = simulated_data['country']
sim_engagement = simulated_data['engagement']
sim_min_support = simulated_data['min_support']

# FP-Growth call for testing
best_tags = perform_fpgrowth(sim_start_date, sim_end_date, sim_country, sim_engagement, sim_min_support)