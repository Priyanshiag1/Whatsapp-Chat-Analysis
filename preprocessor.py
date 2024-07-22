import pandas as pd
import re

def preprocess(data):
    # Define the regex pattern for date and time
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m\s-\s'

    # Find all dates in the data
    dates = re.findall(pattern, data)
    # Split messages based on the pattern
    messages = re.split(pattern, data)[1:]

    # Create a DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Clean and convert the date column
    df['message_date'] = df['message_date'].astype(str)
    df['message_date'] = df['message_date'].str.replace('\u202F', ' ').str.strip()
    date_format = '%d/%m/%y, %I:%M %p -'
    df['message_date'] = pd.to_datetime(df['message_date'], format=date_format, errors='coerce')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract user and message information
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'^([\w\s]+?):\s', message)
        if entry[1:]:  # If there's a user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()

    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

