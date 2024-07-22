from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji

extract= URLExtract()
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_media_messages= df[df['message'] == '<Media omitted>\n'].shape[0]
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words),num_media_messages,len(links)
def most_busy_user(df):
    x = df['user'].value_counts().head()
    df = user_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})

    return x,df
from wordcloud import WordCloud

def create_wordcloud(selected_user, df):
    # Initialize text variable
    text = ""

    # Filter dataframe if user is not 'Overall'
    if selected_user != 'Overall':
        filtered_df = df[df['user'] == selected_user]
        if filtered_df.empty:
            st.write(f"No messages found for {selected_user}.")
            return None
        text = filtered_df['message'].str.cat(sep=" ")
    else:
        # For 'Overall', concatenate messages from all users
        text = df['message'].str.cat(sep=" ")



    # Remove unwanted words or phrases
    unwanted_words = ["Media omitted"]
    for word in unwanted_words:
        text = text.replace(word, "")

    # Generate word cloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(text)

    return df_wc



def most_common_words(selected_user, df):
    # Read stop words from file
    with open(r'C:\Users\BIT\Downloads\stop_hinglish.txt', 'r') as f:
        stop_words = f.read().split()

    # Filter the DataFrame based on selected user
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Remove group notifications and media messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    # Get the 20 most common words
    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Frequency'])

    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_counts = Counter(emojis)

    if not emoji_counts:
        return pd.DataFrame(columns=['emoji', 'count'])  # Return an empty DataFrame with correct column names

    # Create DataFrame with columns 'emoji' and 'count'
    emoji_df = pd.DataFrame(emoji_counts.most_common(len(emoji_counts)), columns=['emoji', 'count'])
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Check if df is empty after filtering
    if df.empty:
        return pd.DataFrame()  # Return an empty DataFrame or handle as needed

    # Create the timeline DataFrame
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    # Generate the 'time' list
    timeline['time'] = timeline.apply(lambda row: f"{row['month']}-{row['year']}", axis=1)

    return timeline
def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # Ensure daily_timeline is always initialized
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline
def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()
def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()
def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap





