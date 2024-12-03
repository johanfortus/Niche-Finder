import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import kagglehub
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

path = kagglehub.dataset_download("asaniczka/trending-youtube-videos-113-countries")
csv_file_path = os.path.join(path, 'trending_yt_videos_113_countries.csv')

df = pd.read_csv(csv_file_path)

def perform_kmeans(start_date, end_date, country, engagement):
    print('PERFORMING K-MEANS')
    print('------------------')
    print('User Input: ')
    print(f'Start Data: {start_date}')
    print(f'End Date: {end_date}')
    print(f'Country: {country}')
    print(f'Engagement: {engagement}')
    print()

    # Filter out data based on user's search attribute input
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

    # Apply scaling
    scaler = StandardScaler()
    df_filtered['view_count_log'] = np.log1p(df_filtered['view_count'])
    df_filtered['like_count_log'] = np.log1p(df_filtered['like_count'])
    df_filtered['comment_count_log'] = np.log1p(df_filtered['comment_count'])
    df_filtered[['view_count_T', 'like_count_T', 'comment_count_T']] = scaler.fit_transform(df_filtered[['view_count_log', 'like_count_log', 'comment_count_log']])

    # Perform K-Means
    kmeans = KMeans(n_clusters = 3)
    kmeans.fit(df_filtered[['view_count_T', 'like_count_T']])
    df_filtered['kmeans_3'] = kmeans.labels_

    scatter_data = df_filtered[['title', 'channel_name', 'thumbnail_url', 'video_id', 'channel_id', 'view_count_T', 'like_count_T', 'comment_count_T', 'kmeans_3']].to_dict(orient='records')
    print(f'Scatter Data: {scatter_data}')
    return scatter_data
    # Plot result
    # plt.scatter(x = df_filtered['view_count_T'], y = df_filtered['like_count_T'], c = df_filtered['kmeans_3'])
    # plt.xlabel('View Count (Scaled)')
    # plt.ylabel('Like Count (Scaled)')
    # plt.show()




# FOR DEVELOPMENT PURPOSES
# determine optimal number clusters through an elbow plot: optimise_k_means(df[['view_count_T', 'like_count_T']], 10)
# https://www.youtube.com/watch?v=iNlZ3IU5Ffw
def optimise_k_means(data, max_k):
    means = []
    inertias = []

    for k in range(1, max_k):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(data)

        means.append(k)
        inertias.append(kmeans.inertia_)

    # Elbow plot
    fig = plt.subplots(figsize=(10,5))
    plt.plot(means, inertias, 'o-')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.grid(True)
    plt.show()


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


class VideoExample:
    def __init__(self, title, channel_name, view_count, like_count, comment_count):
        self.title = title
        self.channel_name = channel_name
        self.view_count = view_count
        self.like_count = like_count
        self.comment_count = comment_count

simulated_data = {
    'searchType': 'k-means',
    'dateRange': {'start': '2024-11-25', 'end': '2024-11-30'},
    'country': 'US',
    'engagement': '72',
    'tags': []
}
sim_start_date = simulated_data['dateRange']['start']
sim_end_date = simulated_data['dateRange']['end']
sim_country = simulated_data['country']
sim_engagement = simulated_data['engagement']
# print(f'Start Date: {sim_start_date}')
# print(f'End Date: {sim_end_date}')
# print(f'Country: {sim_country}')
# print(f'Engagement: {sim_engagement}')
# print(perform_kmeans(sim_start_date, sim_end_date, sim_country, sim_engagement))

# sim_video = VideoExample('How Much Tape To Stop A Lamborghini?', 'MrBeast', 177811809, 5251977, 6791)

# print(calc_engagement_rate(sim_video))