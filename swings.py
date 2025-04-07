# Data analysis and manipulation
import numpy as np
import pandas as pd
from datetime import datetime

# To calculate Swing Highs and Lows
from scipy.signal import *

# To Plot
import matplotlib.pyplot as plt
import warnings 
warnings.filterwarnings('ignore')

relative_path = "data_modules/"
file_name = "Jan_2010_to_Jan_2019_Rebased_Series"
file_extension = ".csv"

data = pd.read_csv(relative_path + file_name + file_extension, index_col=0, parse_dates=True)

data.index = pd.to_datetime(data.index)

# Create a high-low dataset
high_low = data[['rebased_high', 'rebased_low', 'rebased_close']]

argrel_window = 20

# argrelextrema comes from scipy.signal
highs_list = argrelextrema(
    high_low['rebased_high'].values, np.greater, order=argrel_window)
lows_list = argrelextrema(
    high_low['rebased_low'].values, np.less, order=argrel_window)

high_low['swing_low'] = high_low.iloc[lows_list[0], 1]
high_low['swing_high'] = high_low.iloc[highs_list[0], 0]

high_low_preprocess = high_low.copy()

# print(high_low.head(2))

# Plot the graph
# high_low[['rebased_close', 'swing_low', 'swing_high']].plot(
#     style=['k-', 'r*', 'g*'], figsize=(10, 7))
# plt.title('Swings', fontsize=16)
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('SwingHighs_SwingLows', fontsize=14)

# # Add legend to the plot
# plt.legend()
# # Add grid to the plot
# plt.grid()
# # Display the graph
# plt.show()


high_low['swing_high_low'] = high_low['swing_low'].sub(
    high_low['swing_high'], fill_value=0)

high_low = high_low.dropna(subset=['swing_high_low']).copy()

high_low.loc[(high_low['swing_high_low'].shift(1) * high_low['swing_high_low'] < 0) &
             (high_low['swing_high_low'].shift(1) < 0) & (np.abs(high_low['swing_high_low'].shift(1)) < high_low['swing_high_low']), 'swing_high_low'] = np.nan

# print(high_low.head())

high_low.loc[(high_low['swing_high_low'].shift(1) * high_low['swing_high_low'] > 0) &
             (high_low['swing_high_low'].shift(1) < high_low['swing_high_low']), 'swing_high_low'] = np.nan

high_low.loc[(high_low['swing_high_low'].shift(-1) * high_low['swing_high_low'] > 0) &
             (high_low['swing_high_low'].shift(-1) < high_low['swing_high_low']), 'swing_high_low'] = np.nan

high_low = high_low.dropna(subset=['swing_high_low']).copy()


# Instantiate start
i = 0
# Drop all rows with no swing
high_low = high_low.dropna(subset=['swing_high_low']).copy()

while ((high_low['swing_high_low'].shift(1) * high_low['swing_high_low'] > 0)).any():
    # Eliminate the lows higher than highs
    high_low.loc[(high_low['swing_high_low'].shift(1) * high_low['swing_high_low'] < 0) &
                 (high_low['swing_high_low'].shift(1) < 0) & (np.abs(high_low['swing_high_low'].shift(1)) < high_low['swing_high_low']), 'swing_high_low'] = np.nan
    # Eliminates earlier lower values
    high_low.loc[(high_low['swing_high_low'].shift(1) * high_low['swing_high_low'] > 0) &
                 (high_low['swing_high_low'].shift(1) < high_low['swing_high_low']), 'swing_high_low'] = np.nan
    # Eliminates subsequent lower values
    high_low.loc[(high_low['swing_high_low'].shift(-1) * high_low['swing_high_low'] > 0) &
                 (high_low['swing_high_low'].shift(-1) < high_low['swing_high_low']), 'swing_high_low'] = np.nan
    # Reduce the dataframe
    high_low = high_low.dropna(subset=['swing_high_low']).copy()
    i += 1
    # Avoid infinite loop
    if i == 4:
        break


# Join with existing dataframe as pandas cannot join columns with the same headers
# Check if the columns are in the dataframe
if 'swing_low' in data.columns:
     # If so, drop them
    data.drop(['swing_low', 'swing_high'], axis=1, inplace=True)
# Then, join swing high lows
data = data.join(high_low[['swing_low', 'swing_high']])


# Prepare for the Last swing adjustment, if the last_sign <0: swing high, if > 0 swing low
last_swing = np.sign(high_low['swing_high_low'][-1])

# Instantiate last swing high and low dates
last_swing_low_dates = data[data['swing_low'] > 0].index.max()
last_swing_high_dates = data[data['swing_high'] > 0].index.max()

# Print the last swing low dates
# print(last_swing_low_dates)


# Print the last swing high dates
# print(last_swing_high_dates)

# Swing_high_date is not equal to highest high date since swing_low
if (last_swing == -1) & (last_swing_high_dates != data[last_swing_low_dates:]['swing_high'].idxmax()):
    # Reset swing_high to NaN
    data.loc[last_swing_high_dates, 'swing_high'] = np.nan
# Swing_high_date is not equal to highest high date since swing_low
elif (last_swing == 1) & (last_swing_low_dates != data[last_swing_high_dates:]['swing_low'].idxmax()):
    # Reset swing_low to NaN
    data.loc[last_swing_low_dates, 'swing_low'] = np.nan


# This is the dataframe with raw swing highs and lows.
# high_low_preprocess[['rebased_close', 'swing_low', 'swing_high']].plot(
#     style=['k-', 'r*', 'g*'], figsize=(10, 7))

# This is the high_low dataframe after the alternation process
# high_low[['rebased_close', 'swing_low', 'swing_high']].plot(
#     style=['k-', 'r*', 'g*'], figsize=(10, 7))

# This is the main dataframe after joining. Note the adjustments: consecutive lows/highs, lows<highs and last swing
# data[['rebased_close', 'swing_low', 'swing_high']].plot(
#     style=['k-', 'r*', 'g*'], figsize=(10, 7))
# plt.show()



# Creating a function for all above steps
def swings(df, high, low, argrel_window):

    # Create swings:

    # Step 1: copy existing df. We will manipulate and reduce this df and want to preserve the original
    high_low = df[[high, low]].copy()

    # Step 2: build 2 lists of highs and lows using argrelextrema
    highs_list = argrelextrema(
        high_low[high].values, np.greater, order=argrel_window)
    lows_list = argrelextrema(
        high_low[low].values, np.less, order=argrel_window)

    # Step 3: Create swing high and low columns and assign values from the lists
    swing_high = 's' + str(high)[-12:]
    swing_low = 's' + str(low)[-12:]
    high_low[swing_low] = high_low.iloc[lows_list[0], 1]
    high_low[swing_high] = high_low.iloc[highs_list[0], 0]

# Alternation: We want highs to follow lows and keep the most extreme values

    # Step 4. Create a unified column with peaks<0 and troughs>0
    swing_high_low = str(high)[:2]+str(low)[:2]
    high_low[swing_high_low] = high_low[swing_low].sub(
        high_low[swing_high], fill_value=0)

    # Step 5: Reduce dataframe and alternation loop
    # Instantiate start
    i = 0
    # Drops all rows with no swing
    high_low = high_low.dropna(subset=[swing_high_low]).copy()
    while ((high_low[swing_high_low].shift(1) * high_low[swing_high_low] > 0)).any():
        # eliminate lows higher than highs
        high_low.loc[(high_low[swing_high_low].shift(1) * high_low[swing_high_low] < 0) &
                     (high_low[swing_high_low].shift(1) < 0) & (np.abs(high_low[swing_high_low].shift(1)) < high_low[swing_high_low]), swing_high_low] = np.nan
        # eliminate earlier lower values
        high_low.loc[(high_low[swing_high_low].shift(1) * high_low[swing_high_low] > 0) & (
            high_low[swing_high_low].shift(1) < high_low[swing_high_low]), swing_high_low] = np.nan
        # eliminate subsequent lower values
        high_low.loc[(high_low[swing_high_low].shift(-1) * high_low[swing_high_low] > 0) & (
            high_low[swing_high_low].shift(-1) < high_low[swing_high_low]), swing_high_low] = np.nan
        # reduce dataframe
        high_low = high_low.dropna(subset=[swing_high_low]).copy()
        i += 1
        if i == 4:  # avoid infinite loop
            break

    # Step 6: Join with existing dataframe as pandas cannot join columns with the same headers
    # First, we check if the columns are in the dataframe
    if swing_low in df.columns:
        # If so, drop them
        df.drop([swing_low, swing_high], axis=1, inplace=True)
    # Then, join columns
    df = df.join(high_low[[swing_low, swing_high]])

# Last swing adjustment:

    # Step 7: Preparation for the Last swing adjustment
    high_low[swing_high_low] = np.where(
        np.isnan(high_low[swing_high_low]), 0, high_low[swing_high_low])
    # If last_sign <0: swing high, if > 0 swing low
    last_sign = np.sign(high_low[swing_high_low][-1])

    # Step 8: Instantiate last swing high and low dates
    last_slo_dt = df[df[swing_low] > 0].index.max()
    last_shi_dt = df[df[swing_high] > 0].index.max()

    # Step 9: Test for extreme values
    if (last_sign == -1) & (last_shi_dt != df[last_slo_dt:][swing_high].idxmax()):
            # Reset swing_high to nan
        df.loc[last_shi_dt, swing_high] = np.nan
    elif (last_sign == 1) & (last_slo_dt != df[last_shi_dt:][swing_low].idxmax()):
        # Reset swing_low to nan
        df.loc[last_slo_dt, swing_low] = np.nan

    return (df)

# Plot the graphs
data = swings(df=data, high='High', low='Low', argrel_window=20)
data = swings(df=data, high='rebased_high',
              low='rebased_low', argrel_window=20)
data[['Close', 'sLow', 'sHigh', 'rebased_close', 'srebased_low', 'srebased_high']].plot(
    style=['k:', 'r*', 'g*', 'k-', 'r*', 'g*'], figsize=(10, 7))
plt.show()