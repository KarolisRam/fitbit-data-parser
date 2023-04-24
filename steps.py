# made by ChatGPT, plots daily steps nicely.
import os
import pandas as pd
import plotly.express as px

# Specify the folder path containing the json files
folder_path = "fitbit-data/Physical Activity"

# Get a list of all json files in the folder
files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.json') and f.startswith('steps')]

# Read all json files into a list of dataframes
dfs = [pd.read_json(file) for file in files]

# Concatenate all dataframes into a single dataframe
df = pd.concat(dfs)

# Convert dateTime column to datetime type
df['dateTime'] = pd.to_datetime(df['dateTime'], format='%m/%d/%y %H:%M:%S')

# Add a new column for the date only
df['date'] = df['dateTime'].dt.date

# Convert value column to numeric type
df['value'] = pd.to_numeric(df['value'])

# Group by date and sum the values
daily_sum = df.groupby('date')['value'].sum().reset_index()

# Create a plotly bar chart
fig = px.bar(daily_sum, x='date', y='value', title='Steps per Day')
fig.show()
