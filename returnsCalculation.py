# For Data Manipulation
import pandas as pd
# For Numerical Calculations
import numpy as np

# To plot graph
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

relative_path = "./data_modules/"
file_name = "Jan_2010_to_Jan_2019_Rebased_Series"
file_extension = ".csv"

data = pd.read_csv(relative_path + file_name + file_extension, index_col=0 ,parse_dates=True)
# print(data.head(2))

# Below not needed, index_col=0 does the same thing (giving different results somehow)
# data.index = pd.to_datetime(data.index)

# print(data.head(2))

# data[['Close', 'rebased_close']].plot(figsize=(10, 7))

# plt.title('Closed vs Rebased Close')
# plt.ylabel('Price')
# plt.xlabel('Date')
# Legend shows automatically when .plot() is used to plot multiple graphs, below can be used to remove it 
# plt.legend().remove()
# plt.grid()
# plt.show()





# Arithmetic Returns

# Calculate Percentage Change
data['arithmetic_return'] = data['rebased_close'].pct_change()

# Dropping NAN values
data['arithmetic_return'].dropna(inplace=True)

# print(data)

# Plotting Histogram of arithmetic returns
# plt.figure(figsize=[10, 7])
# plt.hist(data['arithmetic_return'], bins=10)
# plt.title('Arithmetic Returns', fontsize=16)
# plt.xlabel('Daily Returns', fontsize=14)
# plt.ylabel('Number of Days',fontsize=14)
# plt.show()

# Cumulative Arithmetic Returns
data['cumulative_arithmetic_return'] = data['arithmetic_return'].cumsum()

# Dropping NAN Values
data['cumulative_arithmetic_return'].dropna(inplace=True)

# Plot the cumulative arithmetic return
# data['cumulative_arithmetic_return'].plot(figsize=(10, 7))
# plt.title('Cumulative Arithmetic Returns', fontsize=16)
# plt.ylabel('Returns', fontsize=14)
# plt.xlabel('Year', fontsize=14)
# plt.legend()
# plt.show()






# Logarithmic Returns
data['log_returns'] = np.log(data['rebased_close']/data['rebased_close'].shift(1))
data['log_returns'].dropna(inplace=True)

# Plotting the histogram 
# plt.figure(figsize=[10, 7])
# plt.hist(data['log_returns'], bins=10)
# plt.title('Logarithmic Returns', fontsize=16)
# plt.xlabel('Daily Log Returns', fontsize=14)
# plt.ylabel('Number of days', fontsize=14)
# plt.grid()
# plt.show()

# Cumulative Log Returns
data['cumulative_log_return'] = data['log_returns'].cumsum()
data['cumulative_log_return'].dropna(inplace=True)

# Plotting Cumulative Graph
# data['cumulative_log_return'].plot(figsize=(10, 7))
# plt.title('Cumulative Logarithmic Returns', fontsize=16)
# plt.ylabel('Returns', fontsize=14)
# plt.xlabel('Year', fontsize=14)
# plt.legend()
# plt.grid()
# plt.show()




# Comparison between Cumulative Arithmetic and Cumulative Logarithmic Returns
plt.figure(figsize=(10, 7))
plt.plot(data[['cumulative_arithmetic_return', 'cumulative_log_return']])
plt.title('Cumulative Arithmetic vs Logarithmic Returns', fontsize=16)
plt.ylabel('Returns', fontsize=14)
plt.xlabel('Year', fontsize=14)

# Adding Legeneds
line_up, = plt.plot(data['cumulative_arithmetic_return'], label='Cumulative Arithmetic Return')
line_down, = plt.plot(data['cumulative_log_return'], label='Cumulative Logarithmic Returns')

plt.legend(handles=[line_up, line_down])
plt.legend()
plt.grid()
plt.show()

