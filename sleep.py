# made by ChatGPT, shows sleep times from to over years.
import os
import json
import datetime
import plotly.graph_objects as go

# Set your folder path
folder_path = 'fitbit-data/Sleep'

# Parse the JSON files and extract sleep start and end times
sleep_data = []
for file in os.listdir(folder_path):
    if file.startswith("sleep-") and file.endswith(".json"):
        with open(os.path.join(folder_path, file), 'r') as f:
            data = json.load(f)
            for sleep_log in data:
                start_time = datetime.datetime.fromisoformat(sleep_log['startTime'])
                end_time = datetime.datetime.fromisoformat(sleep_log['endTime'])

                if end_time.date() != start_time.date():
                    sleep_data.append(
                        (start_time, start_time.replace(hour=23, minute=59, second=59, microsecond=999999)))
                    sleep_data.append((end_time.replace(hour=0, minute=0, second=0, microsecond=0), end_time))
                else:
                    sleep_data.append((start_time, end_time))


def time_to_minutes_since_midnight(time):
    return time.hour * 60 + time.minute


# Create a plotly chart
fig = go.Figure()

for start, end in sleep_data:
    fig.add_trace(go.Scatter(x=[start.date(), end.date()],
                             y=[time_to_minutes_since_midnight(start.time()) / 60,
                                time_to_minutes_since_midnight(end.time()) / 60],
                             mode='lines',
                             line=dict(color='blue', width=1), showlegend=False))

fig.update_xaxes(type='date', title='Date')
fig.update_yaxes(title='Hour', range=[0, 24], dtick=1)
fig.update_layout(title='Daily Sleep Schedule')

fig.show()
