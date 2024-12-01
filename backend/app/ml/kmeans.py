from sklearn.cluster import KMeans
import pandas as pd
import kagglehub
import os

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

    print(df_filtered)

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
    'country': 'Spain',
    'engagement': '72',
    'tags': ['sports', 'soccer']
}
sim_start_date = simulated_data['dateRange']['start']
sim_end_date = simulated_data['dateRange']['end']
sim_country = simulated_data['country']
sim_engagement = simulated_data['engagement']
# print(f'Start Date: {sim_start_date}')
# print(f'End Date: {sim_end_date}')
# print(f'Country: {sim_country}')
# print(f'Engagement: {sim_engagement}')
print(perform_kmeans(sim_start_date, sim_end_date, sim_country, sim_engagement))

# sim_video = VideoExample('How Much Tape To Stop A Lamborghini?', 'MrBeast', 177811809, 5251977, 6791)

# print(calc_engagement_rate(sim_video))