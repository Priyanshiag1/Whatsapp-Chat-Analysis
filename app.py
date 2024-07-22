import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)



    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_messages,links= helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(links)
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color = 'green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.title("Daily Timeline")
        timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['only_date'], timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.title("Activity Map")
        col1,col2= st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
        # Plotting
        fig, ax = plt.subplots()
        ax.bar(busy_day.index, busy_day.values,color='yellow')
        plt.xticks(rotation='vertical')
        plt.xlabel('Day of the Week')
        plt.ylabel('Count')
        plt.title('Most Busy Day of the Week')
        st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            # Plotting
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values,color='orange')
        plt.xticks(rotation='vertical')
        plt.xlabel('Month of the Year')
        plt.ylabel('Count')
        plt.title('Most Busy Month of the Year')
        st.pyplot(fig)
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
    st.title("Most Common Words")
    most_common_df = helper.most_common_words(selected_user, df)
    fig, ax = plt.subplots()
    ax.barh(most_common_df['Word'], most_common_df['Frequency'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
    st.dataframe(most_common_df)
    emoji_df = helper.emoji_helper(selected_user, df)

    st.title("Emoji Analysis")
    col1, col2 = st.columns(2)
    with col1:
        if emoji_df is None or emoji_df.empty:
            st.error("No emoji data found.")
        else:
            st.dataframe(emoji_df)

    with col2:
        if emoji_df is None or emoji_df.empty:
            st.error("No emoji data found.")
        elif 'emoji' not in emoji_df.columns or 'count' not in emoji_df.columns:
            st.error("Invalid DataFrame structure.")
        else:
            # Sort by 'count' in descending order and select the top 5
            top_5_emoji_df = emoji_df.sort_values(by='count', ascending=False).head(5)

            fig, ax = plt.subplots()

            # Plot horizontal bar graph for the top 5 emojis
            ax.barh(top_5_emoji_df['emoji'], top_5_emoji_df['count'], color='skyblue')

            # Add labels and title
            ax.set_xlabel('Count')
            ax.set_ylabel('Emoji')
            ax.set_title('Top 5 Emojis by Frequency')

            st.pyplot(fig)
