from sklearn.cluster import KMeans
import pandas as pd
import kagglehub
import os

path = kagglehub.dataset_download("asaniczka/trending-youtube-videos-113-countries")
csv_file_path = os.path.join(path, 'trending_yt_videos_113_countries.csv')

df = pd.read_csv(csv_file_path)
print(df.head())

def perform_kmeans(start_date, end_date, country, engagement):
    print('PERFORMING K-MEANS')
    print('------------------')
    print('User Input: ')
    print(f'Start Data: {start_date}')
    print(f'End Date: {end_date}')
    print(f'Country: {country}')
    print(f'Engagement: {engagement}')

def calc_engagement_rate(video):
    # High Engagement(above 5 %): 67 - 100
    # Medium Engagement(between 2 % and 5 %): 33 - 66
    # Low Engagement(between 0 % and 2 %): 0 - 32
    print(f'Title: {video.title}')
    print(f'Channel: {video.channel_name}')
    print(f'Views: {video.view_count}')
    print(f'Likes: {video.like_count}')
    print(f'Comments: {video.comment_count}')

    engagement_rate = ((video.like_count + video.comment_count)/video.view_count) * 100
    print(f'Engagement Rate: {round(engagement_rate, 2)}%')

    if engagement_rate >= 5:
        return 'High'
    elif engagement_rate >= 2 and engagement_rate < 5:
        return 'Moderate'
    elif engagement_rate >= 0 and engagement_rate < 2:
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
    'dateRange': {'start': '2024-11-01', 'end': '2024-11-17'},
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
# print(perform_kmeans(sim_start_date, sim_end_date, sim_country, sim_engagement))

sim_video = VideoExample('How Much Tape To Stop A Lamborghini?', 'MrBeast', 177811809, 5251977, 6791)

print(calc_engagement_rate(sim_video))