# For Data Manipulation
import pandas as pd
import numpy as np

# For Graph Plotting
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

relative_path = "../data_modules/"
file_name = "Jan_2010_to_Jan_2019_Rebased_Series"
file_extension = ".csv"

data = pd.read_csv(relative_path + file_name + file_extension, index_col=0, parse_dates=True)

data.index = pd.to_datetime(data.index)

# print(data.head(2))

# Number of trading days in a year or 52 weeks
breakout_window = 252

data['rolling_high'] = data.rebased_high.rolling(window=breakout_window, min_periods=breakout_window).max()

data['rolling_low'] = data.rebased_low.rolling(window=breakout_window, min_periods=breakout_window).min()

# print(data.tail(2))

data['regime_breakout_252'] = np.where(data['rebased_high'] >= data['rolling_high'], 1, 0)


# Plotting a Graph
def plot_graph(data, ylabel, xlabel, title, legend):
    plt.figure(figsize=(10, 7))
    plt.plot(data)
    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.legend(labels=legend)
    plt.grid()
    plt.show()

# ax1 = plot_graph(data[['rebased_high', 'rolling_high']], "Price", "Year", "Rolling & Rebased High", ['rebased_high', 'rolling_high'])

# ax2 = plot_graph(data['regime_breakout_252'], "Signal", "Year", "Regime Breakout", ['regime_breakout_252'])



# Plotting above graphs together
# ax = data[['rebased_high', 'rolling_high']].plot(figsize=(10, 7))
# ax2 = data['regime_breakout_252'].plot(secondary_y=True, figsize=(10, 7), ax=ax)
# ax.set_ylabel('Price', fontsize=14)
# ax.set_xlabel('Year', fontsize=14)
# ax2.set_ylabel('Signal', fontsize=14)
# ax2.set_title('Regime Breakout', fontsize=16)
# plt.legend()
# plt.grid()
# plt.show()





# Regime Breakdown
data['regime_breakdown_252'] = np.where(data['rebased_low'] <= data['rolling_low'], -1, 0)

# ax1 = plot_graph(data[['rebased_low', 'rolling_low']], "Price", "Year", "Rolling & Rebased Low", ['rebased_low', 'rolling_low'])

# ax2 = plot_graph(data['regime_breakdown_252'], "Signal", "Year", "Regime Breakdown", ['regime_breakdown_252'])

# Plotting both graphs together
# ax = data[['rebased_low', 'rolling_low']].plot(figsize=(10, 7))
# ax2 = data['regime_breakdown_252'].plot(secondary_y=True, figsize=(10, 7), ax=ax)
# ax.set_ylabel('Price', fontsize=14)
# ax.set_xlabel('Year', fontsize=14)
# ax2.set_ylabel('Signal', fontsize=14)
# ax.set_title("Regime Breakdown", fontsize=16)
# plt.legend()
# plt.grid()
# plt.show()



# Regime Breakout-Breakdown
# data[['rebased_low', 'rolling_low', 'rebased_high', 'rolling_high']].plot(figsize=(10, 7))
# plt.title('Rolling & Rebased: High & Low', fontsize=16)
# plt.ylabel('Price', fontsize=14)
# plt.xlabel('Year', fontsize=14)
# plt.legend()
# plt.grid()
# plt.show()


# Combining above with both breakout & breakdown signals
# data['regime_breakout_breakdown_252'] = np.where(data['rebased_high'] >= data['rolling_high'], 1, np.where(data['rebased_low'] <= data['rolling_low'], -1, 0))
# # Plotting above graph
# ax = data[['rebased_low', 'rolling_low', 'rebased_high', 'rolling_high']].plot(figsize=(10, 7))
# ax2 = data['regime_breakout_breakdown_252'].plot(secondary_y=True, figsize=(10, 7), ax = ax)
# ax.set_title('Regime Breakout-Breakdowns', fontsize=16)
# ax.set_ylabel('Price', fontsize=14)
# ax2.set_ylabel('Signal', fontsize=14)
# plt.legend()
# plt.grid()
# plt.show()



# Creating a function incorporating the whole file
def regime_breakout_breakdown(breakout_window, df, high, low):
    rolling_high = df[high].rolling(window=breakout_window, min_periods=breakout_window).max()
    rolling_low = df[low].rolling(window=breakout_window, min_periods=breakout_window).min()
    df['regime_breakout_'+str(breakout_window)] = np.where(df[high] > df['rolling_high'], 1, 0)
    df['regime_breakdown_'+str(breakout_window)] = np.where(df[low] < df['rolling_low'], -1, 0)
    df['regime_breakout_breakdown_'+str(breakout_window)] = np.where(df['rebased_high'] >= df['rolling_high'], 1, np.where(df['rebased_low'] <= df['rolling_low'], -1, 0))

    return(data)



print(regime_breakout_breakdown(252, data, 'rebased_high', 'rebased_low'))
