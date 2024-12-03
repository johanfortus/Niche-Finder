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


def perform_fpgrowth(start_date, end_date, country, engagement, min_support=0.001):
    print('PERFORMING FP-GROWTH')
    print('-------------------')
    print('User Input: ')
    print(f'Start Date: {start_date}')
    print(f'End Date: {end_date}')
    print(f'Country: {country}')
    print(f'Engagement: {engagement}')
    print(f'Min Support: {min_support}')
    print()

    # load dataset from Kaggle
    csv_dir_path = asaniczka_trending_youtube_videos_113_countries_path
    csv_file_path = os.path.join(csv_dir_path, 'trending_yt_videos_113_countries.csv')
    try:
        df = pd.read_csv(csv_file_path, encoding='utf-8')
        # Print the first two rows to verify the data is read correctly
        print("First rows of CSV file:")
        print(df.head(2))
    except FileNotFoundError:
        print(f"Dataset file '{csv_file_path}' not found.")
        return None

    # print the columns to verify
    print("Columns in DataFrame:", df.columns.tolist())

    # country column check
    if 'country' not in df.columns:
        print("The dataset does not contain a 'country' column.")
        return None

    # Check for missing values in the country column
    if df['country'].isna().all():
        print("The country column is completely empty. Please check the dataset.")
        return None

    # Filter by country
    df = df[df['country'] == country]
    if df.empty:
        print(f"No data available for the country: {country}")
        return None

    # date and time conversion
    if 'publish_date' in df.columns:
        # Use flexible date parsing to handle different formats
        df['publish_date'] = pd.to_datetime(df['publish_date'], errors='coerce')
        date_column = 'publish_date'
    else:
        print("No suitable date column ('publish_date') found in the dataset.")
        return None

    # filters invalid dates
    df = df.dropna(subset=[date_column])

    # Ensure start_date and end_date are in datetime format
    start_date = pd.to_datetime(start_date, errors='coerce')
    end_date = pd.to_datetime(end_date, errors='coerce')

    # Filter by date range
    mask = (df[date_column] >= start_date) & (df[date_column] <= end_date)
    df = df.loc[mask]
    if df.empty:
        print(f"No data available in the date range: {start_date} to {end_date}")
        return None

    # Debug: Print the range of dates available in the dataset
    print("Available publish date range:", df[date_column].min(), "to", df[date_column].max())

    # Debug: Print unique country codes in the dataset
    print("Unique country codes in dataset:", df['country'].unique())

    # engagement rate calculation
    df['engagement_rate'] = ((df['like_count'] + df['comment_count']) / df['view_count']) * 100
    df['engagement_rate'] = df['engagement_rate'].replace([float('inf'), -float('inf')], 0).fillna(0)

    # filter based on engagement level
    engagement = calc_engagement_rate(engagement)
    if engagement == 'High':
        df_filtered = df[df['engagement_rate'] > 7]
    elif engagement == 'Moderate':
        df_filtered = df[(df['engagement_rate'] >= 3) & (df['engagement_rate'] <= 7)]
    elif engagement == 'Low':
        df_filtered = df[df['engagement_rate'] < 3]
    else:
        df_filtered = df.copy()

    if df_filtered.empty:
        print("No data found for the given engagement level.")
        return None

    # tag prep for FP-Growth
    if 'video_tags' not in df_filtered.columns:
        print("The dataset does not contain a 'video_tags' column.")
        return None

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
    frequent_itemsets = fpgrowth(df_tags, min_support=min_support, use_colnames=True, max_len=3)

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

    return best_tags

def calc_engagement_rate(engagement):
    engagement = int(engagement)
    if engagement >= 67:
        return 'High'
    elif engagement <= 66 and engagement >= 33:
        return 'Moderate'
    elif engagement <= 32:
        return 'Low'

# Example of using form data input
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
