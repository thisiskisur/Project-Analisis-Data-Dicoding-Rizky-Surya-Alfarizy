import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='dark')

# Pastel color palette
pastel_palette = sns.color_palette("pastel")

# Dashboard Title
st.title('Bike Sharing Dashboard 🚲')

# Load Data
def load_data():
    data = pd.read_csv("dashboard/day_fixed.csv")
    return data

day_df = load_data()

# Filter Date Under Raw Data in Sidebar
st.sidebar.subheader('Filter Data')
min_date = pd.to_datetime(day_df['dteday'].min())
max_date = pd.to_datetime(day_df['dteday'].max())
date_range = st.sidebar.date_input("Date Range", value=(min_date, max_date))
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

# Filter Data Based on Date
filtered_df = day_df[(pd.to_datetime(day_df['dteday']) >= start_date) & (pd.to_datetime(day_df['dteday']) <= end_date)]

# Statistical Total Bike Sharing per Month
st.subheader('👉 Statistical Total Bike Sharing per Month')

day_df['month'] = pd.to_datetime(day_df['dteday']).dt.strftime('%b')
total_bike_sharing_per_month = day_df.groupby('month')['cnt'].sum()

# Sort months in order
total_bike_sharing_per_month = total_bike_sharing_per_month.reindex(
    ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
)

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=total_bike_sharing_per_month.index, y=total_bike_sharing_per_month.values, marker='o', color='skyblue', ax=ax)
ax.set_xlabel('Month')
ax.set_ylabel('Total Bike Sharing')
ax.set_title('Total Bike Sharing per Month')
plt.grid(True)
st.pyplot(fig)

# Total Bike Sharing
total_bike_sharing = day_df['cnt'].sum()
st.write(f"Total Bike Sharing: {total_bike_sharing}")

# Display Filtered Data
st.subheader('👉 Daily Data Order')
st.write(filtered_df)

# Visualization 1: Bike Sharing Count per Season
st.subheader('👉 Bike Sharing Count per Season')
season_counts = filtered_df['season'].value_counts()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=season_counts.index, y=season_counts.values, palette=pastel_palette, ax=ax)
ax.set_xlabel('Season')
ax.set_ylabel('Count')
ax.set_title('Bike Sharing Count per Season')
for i, count in enumerate(season_counts.values):
    plt.text(i, count, str(count), ha='center', va='bottom', fontsize=10)
st.pyplot(fig)

# Visualization 2: Average Bike Sharing Based on Working Day or Holiday
st.subheader('👉 Average Bike Sharing Based on Working Day or Holiday')
workingday_avg = filtered_df.groupby('workingday')['cnt'].mean()
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x=workingday_avg.index, y=workingday_avg.values, palette=pastel_palette, ax=ax)
ax.set_xlabel('Working Day')
ax.set_ylabel('Average Bike Sharing')
ax.set_title('Average Bike Sharing Based on Working Day or Holiday')
for index, value in enumerate(workingday_avg):
    plt.text(index, value, str(round(value, 2)), ha='center', va='bottom', fontsize=10)
st.pyplot(fig)

# Visualization 3: Correlation between Weather Condition and Bike Sharing Rate
st.subheader('👉 Correlation between Weather Condition and Bike Sharing Rate')
selected_weather = st.selectbox('Select Weather Condition:', ['1: Clear', '2: Mist + Cloudy', '3: Light Snow'])
weather_mapping = {'1: Clear': 1, '2: Mist + Cloudy': 2, '3: Light Snow': 3}
filtered_data = filtered_df[filtered_df['weathersit'] == weather_mapping[selected_weather]].groupby('workingday')['cnt'].mean()
filtered_data.index = ['Holiday' if index == 0 else 'Working Day' for index in filtered_data.index]
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x=filtered_data.index, y=filtered_data.values, palette=pastel_palette, ax=ax)
ax.set_xlabel('Day')
ax.set_ylabel('Average Bike Sharing')
ax.set_title('Average Bike Sharing Based on Weather Condition')
for index, value in enumerate(filtered_data):
    plt.text(index, value, str(round(value, 2)), ha='center', va='bottom', fontsize=10)
st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Copyright Iamkisur ©️ 2025 Rizky Surya Alfarizy")