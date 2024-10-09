import pandas as pd
from datetime import datetime, timedelta
import pytz
import sys

# Define the correct column names for the dataset
columns = ['date', 'fajr begins', 'fajr jamaah', 'sunrise', 'zuhr begins', 'zuhr jamaah', 
           'asr begins', 'asr jamaah', 'maghrib begins', 'maghrib jamaah', 'isha begins', 'isha jamaah']

# Load the text file using the custom delimiter '--'
df = pd.read_csv('prayer_times.txt', delimiter='--', header=None, names=columns, engine='python')

# Set the timezone for BST
bst = pytz.timezone('Europe/London')

# Get the current year
current_year = datetime.now().year

# Function to add or subtract minutes to the time
def adjust_minutes(time_str, minutes):
    try:
        # Parse the time string
        time_obj = datetime.strptime(time_str.strip(), '%H:%M')
        # Adjust the time by the specified number of minutes
        adjusted_time = time_obj + timedelta(minutes=minutes)
        # Return the adjusted time as a string
        return adjusted_time.strftime('%H:%M')
    except ValueError:
        # Handle any errors in case of invalid time format
        return time_str

# ------------------------------------
# Process 1: IQAMA Times
# ------------------------------------

# Select columns for iqama: 'fajr jamaah', 'zuhr jamaah', 'asr jamaah', 'maghrib jamaah', 'isha jamaah'
iqama_columns = df[['fajr jamaah', 'zuhr jamaah', 'asr jamaah', 'maghrib jamaah', 'isha jamaah']].copy()

# Add 5 minutes to the 'maghrib jamaah' column
iqama_columns.loc[:, 'maghrib jamaah'] = iqama_columns['maghrib jamaah'].apply(lambda x: adjust_minutes(x, 5))

# Save iqama times to a CSV file
iqama_columns.to_csv('iqama_times.csv', index=False)
print("Iqama times saved to iqama_times.csv")

# ------------------------------------
# Process 2: ATHAN Times
# ------------------------------------

# Select columns for athan: 'fajr jamaah', 'sunrise', 'zuhr jamaah', 'asr jamaah', 'maghrib jamaah', 'isha jamaah'
athan_columns = df[['fajr jamaah', 'sunrise', 'zuhr jamaah', 'asr jamaah', 'maghrib jamaah', 'isha jamaah']].copy()

# Minus minutes to 'fajr jamaah', 'zuhr jamaah', 'asr jamaah', and 'isha jamaah'
athan_columns.loc[:, 'fajr jamaah'] = athan_columns['fajr jamaah'].apply(lambda x: adjust_minutes(x, -15))
athan_columns.loc[:, 'zuhr jamaah'] = athan_columns['zuhr jamaah'].apply(lambda x: adjust_minutes(x, -20))
athan_columns.loc[:, 'asr jamaah'] = athan_columns['asr jamaah'].apply(lambda x: adjust_minutes(x, -20))
athan_columns.loc[:, 'isha jamaah'] = athan_columns['isha jamaah'].apply(lambda x: adjust_minutes(x, -20))

#athan_columns['fajr jamaah'] = athan_columns['fajr jamaah'].apply(lambda x: adjust_minutes(x, -15))
#athan_columns['zuhr jamaah'] = athan_columns['zuhr jamaah'].apply(lambda x: adjust_minutes(x, -20))
#athan_columns['asr jamaah'] = athan_columns['asr jamaah'].apply(lambda x: adjust_minutes(x, -20))
#athan_columns['isha jamaah'] = athan_columns['isha jamaah'].apply(lambda x: adjust_minutes(x, -20))

# Check if the day is Friday and set 'zuhr jamaah' time to 13:00
# Convert the date column to datetime and find the day of the week
day_of_week = pd.to_datetime(df['date'] + f' {current_year}', format='%b %d %Y').dt.dayofweek

# Set 'zuhr jamaah' to '13:00' on Fridays (day_of_week == 4)
athan_columns.loc[day_of_week == 4, 'zuhr jamaah'] = '13:00'

# Save athan times to a CSV file
athan_columns.to_csv('athan_times.csv', index=False)
print("Athan times saved to athan_times.csv")

# Exit the script gracefully
sys.exit("Script completed successfully.")